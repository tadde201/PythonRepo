"""Email delivery helper functions."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional


def send_email(
    subject: str,
    body: str,
    to_address: str,
    from_address: str,
    smtp_server: str = "localhost",
    smtp_port: int = 587,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> bool:
    """
    Send an email notification.
    
    Args:
        subject: Email subject line
        body: Email body content
        to_address: Recipient email address
        from_address: Sender email address
        smtp_server: SMTP server address (default: localhost)
        smtp_port: SMTP server port (default: 587)
        username: SMTP username (optional)
        password: SMTP password (optional)
        
    Returns:
        True if email sent successfully, False otherwise
    """
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = from_address
        message["To"] = to_address
        
        # Add plain text version
        text_part = MIMEText(body, "plain")
        message.attach(text_part)
        
        # Add HTML version with basic formatting
        html_body = f"""
        <html>
            <body>
                <h2>{subject}</h2>
                <pre style="font-family: Arial, sans-serif; white-space: pre-wrap;">
{body}
                </pre>
            </body>
        </html>
        """
        html_part = MIMEText(html_body, "html")
        message.attach(html_part)
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Enable encryption
            
            if username and password:
                server.login(username, password)
            
            server.sendmail(from_address, to_address, message.as_string())
        
        print(f"✓ Email sent successfully to {to_address}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"✗ Email authentication failed: {str(e)}")
        return False
    except smtplib.SMTPException as e:
        print(f"✗ SMTP error occurred: {str(e)}")
        return False
    except Exception as e:
        print(f"✗ Error sending email: {str(e)}")
        return False


def format_email_body(job_matches: list) -> str:
    """
    Format job match results for email body.
    
    Args:
        job_matches: List of job match result dictionaries
        
    Returns:
        Formatted email body string
    """
    if not job_matches:
        return "No job matches found."
    
    body = "CareerMatch AI - Job Matching Results\n"
    body += "=" * 50 + "\n\n"
    
    for i, match in enumerate(job_matches, 1):
        job = match.get("job", {})
        analysis = match.get("match", "No analysis available")
        
        body += f"Job #{i}: {job.get('title', 'Unknown')} @ {job.get('company', 'Unknown')}\n"
        body += f"Location: {job.get('location', 'Not specified')}\n"
        body += f"Match Analysis:\n{analysis}\n"
        body += "-" * 50 + "\n\n"
    
    body += "Best of luck with your applications!\n"
    body += "CareerMatch AI Agent"
    
    return body


def send_match_results_email(
    to_address: str,
    from_address: str,
    job_matches: list,
    smtp_server: str = "localhost",
    smtp_port: int = 587,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> bool:
    """
    Send job matching results via email.
    
    Args:
        to_address: Recipient email address
        from_address: Sender email address
        job_matches: List of job match results
        smtp_server: SMTP server address
        smtp_port: SMTP server port
        username: SMTP username (optional)
        password: SMTP password (optional)
        
    Returns:
        True if email sent successfully, False otherwise
    """
    subject = f"CareerMatch AI - {len(job_matches)} Job Matches Found"
    body = format_email_body(job_matches)
    
    return send_email(
        subject=subject,
        body=body,
        to_address=to_address,
        from_address=from_address,
        smtp_server=smtp_server,
        smtp_port=smtp_port,
        username=username,
        password=password
    )
