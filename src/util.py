from typing import Dict, List
import polars as pl
import re

def extract_emails(df: pl.DataFrame, columns: List[str]) -> List[Dict[str, str]]:
    """Function to clean and extract author names and email addresses"""
    extracted = []
    for c in columns:
        emails = [x[0] for x in df.select(c).rows()]
        for email in emails:
            if not email:
                continue
            for entry in email:
                # Regex to extract email addresses and names
                matches = re.findall(r'([^<>"]+)\s*<([^<>]+)>', entry)
                if not matches:
                    continue
                for name, email_addr in matches:
                    name = name.strip().strip('"')  # Clean up extra quotes and spaces
                    email_addr = email_addr.strip()
                    if any(domain in email_addr for domain in ['juul.com', 'pax.com', 'ploom.com', 'juullabs.com']):
                        extracted.append({'name': name, 'email': email_addr, 'tag': c})
    return extracted