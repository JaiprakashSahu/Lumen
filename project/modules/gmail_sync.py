from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
import re
import hashlib
from modules.llm_extraction.extractor import extract_transaction_from_text, extract_receipt_from_text
from modules.database.transaction_repo import TransactionRepository, ReceiptRepository
from modules.analytics.cache import analytics_cache


def _decode_base64_url(data):
    """Decode Gmail base64url payload into text."""
    if not data:
        return ""

    try:
        missing_padding = len(data) % 4
        if missing_padding:
            data += "=" * (4 - missing_padding)
        return base64.urlsafe_b64decode(data.encode("utf-8")).decode("utf-8", errors="ignore")
    except Exception:
        return ""


def _strip_html_tags(text):
    """Convert basic HTML into readable plain text."""
    if not text:
        return ""
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</p\s*>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _collect_message_text(part, text_chunks):
    """Recursively collect text/plain and text/html body chunks."""
    if not part:
        return

    mime_type = (part.get("mimeType") or "").lower()
    body_data = part.get("body", {}).get("data")

    if mime_type.startswith("text/plain") and body_data:
        decoded = _decode_base64_url(body_data)
        if decoded.strip():
            text_chunks.append(decoded.strip())
    elif mime_type.startswith("text/html") and body_data:
        decoded = _strip_html_tags(_decode_base64_url(body_data))
        if decoded.strip():
            text_chunks.append(decoded.strip())

    for child in part.get("parts", []) or []:
        _collect_message_text(child, text_chunks)


def _header_map(full_msg):
    """Build lowercase header map from Gmail message payload."""
    headers = full_msg.get("payload", {}).get("headers", [])
    return {
        (h.get("name") or "").lower(): h.get("value") or ""
        for h in headers
    }


def _build_llm_email_text(full_msg):
    """Create rich per-message text input for LLM extraction."""
    headers = _header_map(full_msg)
    snippet = full_msg.get("snippet", "")

    chunks = []
    _collect_message_text(full_msg.get("payload", {}), chunks)

    # Fallback: Gmail sometimes stores body directly at payload.body.data
    if not chunks:
        body_data = full_msg.get("payload", {}).get("body", {}).get("data")
        decoded = _decode_base64_url(body_data)
        if decoded.strip():
            chunks.append(decoded.strip())

    body_text = "\n".join(chunks)

    combined_text = (
        f"Subject: {headers.get('subject', '')}\n"
        f"From: {headers.get('from', '')}\n"
        f"To: {headers.get('to', '')}\n"
        f"Date: {headers.get('date', '')}\n"
        f"Snippet: {snippet}\n"
        f"Body:\n{body_text}"
    ).strip()

    # Keep prompt size bounded while still giving enough context.
    return combined_text[:12000]


def _find_first_attachment(part):
    """Recursively find the first attachment metadata in message parts."""
    if not part:
        return None

    filename = part.get("filename")
    attachment_id = part.get("body", {}).get("attachmentId")
    if filename and attachment_id:
        return {
            "filename": filename,
            "attachment_id": attachment_id,
        }

    for child in part.get("parts", []) or []:
        found = _find_first_attachment(child)
        if found:
            return found

    return None


def _user_scope_prefix(user_email):
    """Create stable per-user ID prefix for stored Gmail entities."""
    normalized = (user_email or "").strip().lower()
    digest = hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:10] if normalized else "anon"
    return f"U{digest}_"


def sync_gmail_transactions(session_credentials, user_email):
    """
    Fetch transaction emails from Gmail, extract with LLM, and store in SQLite.
    Only processes new transactions that aren't already in the database.
    """
    creds = Credentials(**session_credentials)
    gmail = build("gmail", "v1", credentials=creds)
    
    # Query for banking and payment transactions
    tx_query = '(from:(bank OR paytm OR phonepe OR gpay OR googlepay OR amazonpay OR paypal OR bhim OR upi OR alerts) OR subject:(transaction OR credited OR debited OR payment OR "account statement" OR "debit card" OR "credit card" OR "net banking" OR UPI OR NEFT OR RTGS OR IMPS)) AND (credited OR debited OR paid OR received OR sent OR withdrawn OR deposited OR transferred OR Rs OR INR OR ₹)'
    
    try:
        result = gmail.users().messages().list(userId="me", q=tx_query, maxResults=50).execute()
        messages = result.get("messages", [])
        
        new_count = 0
        skipped_count = 0
        error_count = 0
        
        for msg in messages:
            try:
                full_msg = gmail.users().messages().get(userId="me", id=msg["id"], format="full").execute()
                llm_input_text = _build_llm_email_text(full_msg)
                
                # Extract transaction info using LLM
                transaction_dict = extract_transaction_from_text(llm_input_text)
                
                # Store ALL transactions, even if extraction partially fails
                if transaction_dict:
                    # Keep one stable ID per Gmail message and user.
                    txn_id = f"{_user_scope_prefix(user_email)}GMAIL_{msg['id']}"
                    transaction_dict['txn_id'] = txn_id
                    transaction_dict['raw_email_snippet'] = llm_input_text

                    # Check for duplicates
                    if not TransactionRepository.exists(transaction_dict['txn_id']):
                        # Also check by date/amount/merchant to avoid duplicates (if amount exists)
                        amount = transaction_dict.get('amount', 0)
                        if amount > 0:
                            duplicate_check = TransactionRepository.check_duplicate(
                                transaction_dict['date'],
                                transaction_dict['amount'],
                                transaction_dict['merchant_name'],
                                user_email=user_email
                            )
                        else:
                            duplicate_check = False
                        
                        if not duplicate_check:
                            success, message = TransactionRepository.add_transaction(transaction_dict)
                            if success:
                                new_count += 1
                            else:
                                error_count += 1
                                print(f"Error storing transaction: {message}")
                        else:
                            skipped_count += 1
                    else:
                        skipped_count += 1
                else:
                    # LLM extraction completely failed
                    error_count += 1
                    print(f"LLM extraction failed for message {msg['id']}")
            except Exception as e:
                error_count += 1
                print(f"Error processing transaction message {msg['id']}: {str(e)}")
        
        return {
            'success': True,
            'new_transactions': new_count,
            'skipped': skipped_count,
            'errors': error_count
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def sync_gmail_receipts(session_credentials, user_email):
    """
    Fetch receipt/invoice emails from Gmail, extract with LLM, and store in SQLite.
    Only processes new receipts that aren't already in the database.
    """
    creds = Credentials(**session_credentials)
    gmail = build("gmail", "v1", credentials=creds)
    
    # Query for payment-related invoices and bills
    invoice_query = '(subject:(invoice OR receipt OR bill OR payment OR "order confirmation" OR "tax invoice") OR from:(payment OR billing OR invoice OR noreply)) has:attachment filename:pdf'
    
    try:
        result = gmail.users().messages().list(userId="me", q=invoice_query, maxResults=50).execute()
        messages = result.get("messages", [])
        
        new_count = 0
        skipped_count = 0
        error_count = 0
        
        for msg in messages:
            try:
                receipt_id = f"{_user_scope_prefix(user_email)}GMAIL_{msg['id']}"

                # Check if this message was already processed for this user.
                if ReceiptRepository.exists(receipt_id):
                    skipped_count += 1
                    continue
                
                full_msg = gmail.users().messages().get(userId="me", id=msg["id"], format="full").execute()
                llm_input_text = _build_llm_email_text(full_msg)
                
                # Extract receipt info using LLM
                receipt_dict = extract_receipt_from_text(llm_input_text)
                
                if receipt_dict:
                    # Keep one stable ID per Gmail message and user.
                    receipt_dict['receipt_id'] = receipt_id

                    # Add attachment information
                    attachment = _find_first_attachment(full_msg.get("payload", {}))
                    if attachment:
                        receipt_dict['attachment_filename'] = attachment["filename"]
                        receipt_dict['attachment_message_id'] = msg["id"]
                        receipt_dict['attachment_id'] = attachment["attachment_id"]
                    
                    # Store raw snippet
                    receipt_dict['raw_snippet'] = llm_input_text
                    
                    # Save to database
                    success, message = ReceiptRepository.add_receipt(receipt_dict)
                    if success:
                        new_count += 1
                    else:
                        error_count += 1
                        print(f"Error storing receipt: {message}")
                else:
                    # LLM extraction failed for receipt
                    error_count += 1
                    print(f"LLM extraction failed for receipt message {msg['id']}")
            except Exception as e:
                error_count += 1
                print(f"Error processing receipt message {msg['id']}: {str(e)}")
        
        return {
            'success': True,
            'new_receipts': new_count,
            'skipped': skipped_count,
            'errors': error_count
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def sync_all_gmail_data(session_credentials, user_email):
    """
    Sync both transactions and receipts from Gmail.
    Additive sync: keeps previous records and inserts only new Gmail messages.
    """
    tx_result = sync_gmail_transactions(session_credentials, user_email)
    receipt_result = sync_gmail_receipts(session_credentials, user_email)

    # Analytics cache should refresh after new data is inserted.
    analytics_cache.clear()
    
    return {
        'transactions': tx_result,
        'receipts': receipt_result
    }
