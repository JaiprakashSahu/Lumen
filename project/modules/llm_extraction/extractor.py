"""
LLM Extraction Module for Project LUMEN
========================================
Extracts structured transaction/receipt data from email text using LLM.

UPDATED: Now uses centralized LLM Router for automatic provider switching.
If local LLM is unavailable, automatically falls back to Groq.
"""

import json
import re
from email.utils import parsedate_to_datetime
from datetime import datetime

# Use centralized LLM router
from modules.llm.router import llm_router


def _extract_header_value(text, header_name):
    """Extract a header value from structured email text."""
    if not text:
        return ""
    pattern = rf"^{re.escape(header_name)}\s*:\s*(.+)$"
    match = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
    return match.group(1).strip() if match else ""


def _fallback_merchant_from_text(text):
    """Infer merchant/sender from From header when LLM extraction fails."""
    sender = _extract_header_value(text, "From")
    if not sender:
        return "Unknown"

    # Handle common forms: Name <email@domain.com>
    sender = sender.split("<", 1)[0].strip().strip('"').strip("'")
    return sender or "Unknown"


def _fallback_date_from_text(text):
    """Infer date from Date header, else fallback to today."""
    date_header = _extract_header_value(text, "Date")
    if date_header:
        try:
            return parsedate_to_datetime(date_header).strftime("%Y-%m-%d")
        except Exception:
            pass
    return datetime.now().strftime('%Y-%m-%d')


def _fallback_amount_from_text(text):
    """Extract the first plausible currency amount from text."""
    if not text:
        return 0.0

    patterns = [
        r"(?:INR|Rs\.?|₹)\s*([0-9][0-9,]*(?:\.[0-9]{1,2})?)",
        r"([0-9][0-9,]*(?:\.[0-9]{1,2})?)\s*(?:INR|Rs\.?|₹)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            try:
                return float(match.group(1).replace(',', ''))
            except (ValueError, TypeError):
                continue

    return 0.0


def _fallback_total_amount_from_text(text):
    """Extract total amount for receipts using total-specific patterns first."""
    if not text:
        return 0.0

    total_patterns = [
        r"total(?:\s+amount)?\s*[:\-]?\s*(?:INR|Rs\.?|₹)?\s*([0-9][0-9,]*(?:\.[0-9]{1,2})?)",
        r"amount\s+paid\s*[:\-]?\s*(?:INR|Rs\.?|₹)?\s*([0-9][0-9,]*(?:\.[0-9]{1,2})?)",
    ]

    for pattern in total_patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            try:
                return float(match.group(1).replace(',', ''))
            except (ValueError, TypeError):
                continue

    return _fallback_amount_from_text(text)


def call_llm_for_info(text):
    """
    Send transaction text to LLM for extraction.
    Returns the raw response text from the LLM.
    
    Now uses LLM Router for automatic local/groq switching.
    """
    prompt = f"""Extract the transaction details from the text below.

Return ONLY this exact format. EACH FIELD MUST BE ON ITS OWN LINE.
NO quotes, NO commas, NO JSON, NO extra text, NO code blocks.

txn_id:
description:
clean_description:
merchant_name:
merchant_type:
payment_channel:
amount:
type:
date:
weekday:
time_of_day:
balance_after_txn:
category:
subcategory:
transaction_mode:
is_recurring:
recurrence_interval:
confidence_score:
is_high_value:
is_suspicious:
embedding_version:

Text:
{text}
"""

    try:
        # Use LLM router (handles local/groq switching automatically)
        result = llm_router.generate_simple(prompt)
        
        if result["success"] and result["content"]:
            print(f"✅ LLM extraction successful (provider: {result.get('provider_used', 'unknown')})")
            return result["content"]
        else:
            print(f"⚠️ LLM extraction failed: {result.get('error', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"❌ LLM API Error: {str(e)}")
        return None


def parse_info_to_dict(info_text):
    """
    Parse the LLM response text into a structured dictionary.
    Handles type conversion and sanitization.
    """
    if not info_text:
        return None
    
    # Initialize result dictionary
    result = {}
    
    # Split by lines and parse key:value pairs
    lines = info_text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if ':' not in line:
            continue
            
        key, value = line.split(':', 1)
        key = key.strip()
        value = value.strip()
        
        # Remove any quotes or extra whitespace
        value = value.strip('"').strip("'").strip()
        
        # Store in result
        result[key] = value
    
    # Sanitize and convert types
    sanitized = sanitize_transaction_dict(result)
    
    return sanitized


def sanitize_transaction_dict(raw_dict):
    """
    Convert string values to appropriate types and add defaults.
    """
    sanitized = {}
    
    # String fields
    sanitized['txn_id'] = raw_dict.get('txn_id', f"TXN_{datetime.now().strftime('%Y%m%d%H%M%S')}")
    sanitized['description'] = raw_dict.get('description', '')
    sanitized['clean_description'] = raw_dict.get('clean_description', '')
    sanitized['merchant_name'] = raw_dict.get('merchant_name', 'Unknown')
    sanitized['payment_channel'] = raw_dict.get('payment_channel', 'Unknown')
    sanitized['weekday'] = raw_dict.get('weekday', '')
    sanitized['time_of_day'] = raw_dict.get('time_of_day', '')
    sanitized['category'] = raw_dict.get('category', 'Other')
    sanitized['subcategory'] = raw_dict.get('subcategory', '')
    sanitized['recurrence_interval'] = raw_dict.get('recurrence_interval') if raw_dict.get('recurrence_interval') else None
    
    # Type field (debit/credit)
    type_value = raw_dict.get('type', '').lower()
    if 'credit' in type_value:
        sanitized['type'] = 'credit'
    elif 'debit' in type_value:
        sanitized['type'] = 'debit'
    else:
        sanitized['type'] = 'debit'  # Default to debit for spending
    
    # Date field (YYYY-MM-DD)
    date_str = raw_dict.get('date', '')
    if date_str and date_str.lower() not in ['', 'unknown', 'none', 'null']:
        sanitized['date'] = date_str
    else:
        sanitized['date'] = datetime.now().strftime('%Y-%m-%d')
    
    # Float fields
    try:
        amount_str = raw_dict.get('amount', '0')
        # Remove currency symbols and commas
        amount_str = str(amount_str).replace('₹', '').replace(',', '').replace('Rs', '').replace('.', '', amount_str.count('.') - 1 if amount_str.count('.') > 1 else 0).strip()
        sanitized['amount'] = float(amount_str) if amount_str else 0.0
    except (ValueError, TypeError):
        sanitized['amount'] = 0.0
    
    try:
        balance_str = raw_dict.get('balance_after_txn', '')
        if balance_str and balance_str.lower() not in ['', 'unknown', 'none', 'null']:
            sanitized['balance_after_txn'] = float(str(balance_str).replace(',', ''))
        else:
            sanitized['balance_after_txn'] = None
    except (ValueError, TypeError):
        sanitized['balance_after_txn'] = None
    
    try:
        sanitized['confidence_score'] = float(raw_dict.get('confidence_score', 0.8))
    except (ValueError, TypeError):
        sanitized['confidence_score'] = 0.8
    
    # Boolean fields
    is_recurring_str = str(raw_dict.get('is_recurring', 'false')).lower()
    sanitized['is_recurring'] = is_recurring_str in ['true', 'yes', '1']
    
    is_suspicious_str = str(raw_dict.get('is_suspicious', 'false')).lower()
    sanitized['is_suspicious'] = is_suspicious_str in ['true', 'yes', '1']
    
    # Integer field
    try:
        sanitized['embedding_version'] = int(raw_dict.get('embedding_version', 1))
    except (ValueError, TypeError):
        sanitized['embedding_version'] = 1
    
    return sanitized


def extract_transaction_from_text(text):
    """
    Complete pipeline: text -> LLM -> parsed dict.
    Falls back to basic extraction if LLM fails.
    """
    info_text = call_llm_for_info(text)
    
    if info_text:
        transaction_dict = parse_info_to_dict(info_text)
        
        # Debug: Print what was parsed
        if transaction_dict:
            print(f"   📝 Parsed: {transaction_dict.get('merchant_name', 'Unknown')} | ₹{transaction_dict.get('amount', 0)} | {transaction_dict.get('category', 'Other')}")
        
        # Accept if we got a valid merchant name (not just defaults)
        if transaction_dict and transaction_dict.get('merchant_name', 'Unknown') != 'Unknown':
            return transaction_dict
        
        # Also accept if we got a valid amount
        if transaction_dict and transaction_dict.get('amount', 0) > 0:
            return transaction_dict
    
    # Fallback: Create basic transaction with raw text if LLM fails
    # This ensures ALL fetched data is stored
    print(f"⚠️ LLM extraction failed, using fallback for: {text[:100]}...")

    fallback_merchant = _fallback_merchant_from_text(text)
    fallback_amount = _fallback_amount_from_text(text)
    fallback_date = _fallback_date_from_text(text)

    return {
        'txn_id': f"TXN_FALLBACK_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
        'description': text,
        'clean_description': text[:200],
        'merchant_name': fallback_merchant,
        'payment_channel': 'Unknown',
        'amount': fallback_amount,
        'type': 'debit',
        'date': fallback_date,
        'weekday': datetime.now().strftime('%A'),
        'time_of_day': datetime.now().strftime('%H:%M'),
        'balance_after_txn': None,
        'category': 'Uncategorized',
        'subcategory': '',
        'is_recurring': False,
        'recurrence_interval': None,
        'confidence_score': 0.0,

        'is_suspicious': False,
        'embedding_version': 1
    }


def call_llm_for_receipt_info(text):
    """
    Send receipt text to LLM for extraction.
    Returns the raw response text from the LLM.
    
    Now uses LLM Router for automatic local/groq switching.
    """
    prompt = f"""Extract the receipt/invoice details from the text below.

Return ONLY this exact format. EACH FIELD MUST BE ON ITS OWN LINE.
NO quotes, NO commas, NO JSON, NO extra text, NO code blocks.

receipt_id:
receipt_type:
issue_date:
issue_time:
merchant_name:
merchant_address:
merchant_gst:
subtotal_amount:
tax_amount:
total_amount:
payment_method:
extracted_confidence_score:
is_suspicious:
embedding_version:

Text:
{text}
"""

    try:
        # Use LLM router (handles local/groq switching automatically)
        result = llm_router.generate_simple(prompt)
        
        if result["success"] and result["content"]:
            print(f"✅ Receipt LLM extraction successful (provider: {result.get('provider_used', 'unknown')})")
            return result["content"]
        else:
            print(f"⚠️ Receipt LLM extraction failed: {result.get('error', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"❌ Receipt LLM API Error: {str(e)}")
        return None


def parse_receipt_to_dict(info_text):
    """
    Parse the LLM response text for receipts into a structured dictionary.
    """
    if not info_text:
        return None
    
    result = {}
    lines = info_text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if ':' not in line:
            continue
            
        key, value = line.split(':', 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'").strip()
        result[key] = value
    
    sanitized = sanitize_receipt_dict(result)
    return sanitized


def sanitize_receipt_dict(raw_dict):
    """
    Convert string values to appropriate types for receipts.
    """
    sanitized = {}
    
    # String fields
    sanitized['receipt_id'] = raw_dict.get('receipt_id', f"RCP_{datetime.now().strftime('%Y%m%d%H%M%S')}")
    sanitized['receipt_type'] = raw_dict.get('receipt_type', 'digital')
    sanitized['issue_date'] = raw_dict.get('issue_date', datetime.now().strftime('%Y-%m-%d'))
    sanitized['issue_time'] = raw_dict.get('issue_time', '')
    sanitized['merchant_name'] = raw_dict.get('merchant_name', 'Unknown')
    sanitized['merchant_address'] = raw_dict.get('merchant_address', '')
    sanitized['merchant_gst'] = raw_dict.get('merchant_gst', '')
    sanitized['payment_method'] = raw_dict.get('payment_method', 'Unknown')
    
    # Float fields
    try:
        amount_str = str(raw_dict.get('subtotal_amount', '0')).replace('₹', '').replace(',', '').strip()
        sanitized['subtotal_amount'] = float(amount_str) if amount_str else 0.0
    except (ValueError, TypeError):
        sanitized['subtotal_amount'] = 0.0
    
    try:
        tax_str = str(raw_dict.get('tax_amount', '0')).replace('₹', '').replace(',', '').strip()
        sanitized['tax_amount'] = float(tax_str) if tax_str else 0.0
    except (ValueError, TypeError):
        sanitized['tax_amount'] = 0.0
    
    try:
        total_str = str(raw_dict.get('total_amount', '0')).replace('₹', '').replace(',', '').strip()
        sanitized['total_amount'] = float(total_str) if total_str else 0.0
    except (ValueError, TypeError):
        sanitized['total_amount'] = 0.0
    
    try:
        sanitized['extracted_confidence_score'] = float(raw_dict.get('extracted_confidence_score', 0.8))
    except (ValueError, TypeError):
        sanitized['extracted_confidence_score'] = 0.8
    
    # Boolean field
    is_suspicious_str = str(raw_dict.get('is_suspicious', 'false')).lower()
    sanitized['is_suspicious'] = is_suspicious_str in ['true', 'yes', '1']
    
    # Integer field
    try:
        sanitized['embedding_version'] = int(raw_dict.get('embedding_version', 1))
    except (ValueError, TypeError):
        sanitized['embedding_version'] = 1
    
    return sanitized


def extract_receipt_from_text(text):
    """
    Complete pipeline for receipt: text -> LLM -> parsed dict.
    Falls back to basic extraction if LLM fails.
    """
    info_text = call_llm_for_receipt_info(text)
    
    if info_text:
        receipt_dict = parse_receipt_to_dict(info_text)
        if receipt_dict and receipt_dict.get('total_amount', 0) > 0:
            return receipt_dict
    
    # Fallback: Create basic receipt with raw text if LLM fails
    # This ensures ALL fetched data is stored
    print(f"⚠️ LLM extraction failed for receipt, using fallback: {text[:100]}...")

    fallback_merchant = _fallback_merchant_from_text(text)
    fallback_total = _fallback_total_amount_from_text(text)
    fallback_date = _fallback_date_from_text(text)

    return {
        'receipt_id': f"RCP_FALLBACK_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
        'receipt_type': 'digital',
        'issue_date': fallback_date,
        'issue_time': datetime.now().strftime('%H:%M'),
        'merchant_name': fallback_merchant,
        'merchant_address': '',
        'merchant_gst': '',
        'subtotal_amount': fallback_total,
        'tax_amount': 0.0,
        'total_amount': fallback_total,
        'payment_method': 'Unknown',
        'extracted_confidence_score': 0.0,
        'is_suspicious': False,
        'embedding_version': 1
    }
