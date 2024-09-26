from typing import Optional, Dict, List, Tuple
import polars as pl
import re

def extract_emails(df: pl.DataFrame, columns: List[str], include_domains: Optional[List[str]] = None, exclude_domains: Optional[List[str]] = None) -> List[Dict[str, str]]:
    """Function to clean and extract author names and email addresses"""
    if include_domains:
        assert not exclude_domains
    else:
        assert not include_domains
        exclude_domains = [] if not exclude_domains else exclude_domains
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
                    if include_domains:
                        if any(domain in email_addr for domain in include_domains):
                            extracted.append({'name': name, 'email': email_addr, 'tag': c})
                    else:
                        if not any(domain in email_addr for domain in exclude_domains):
                            extracted.append({'name': name, 'email': email_addr, 'tag': c})

    return extracted

