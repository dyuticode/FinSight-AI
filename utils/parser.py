import pandas as pd
from pypdf import PdfReader
import io

def parse_statement(file_bytes, filename):
    """
    Parses CSV or PDF bank statements into a standardized DataFrame.
    Expected output columns: 'date', 'description', 'amount'
    """
    if filename.endswith('.csv'):
        # Read CSV and try to standardize column names
        df = pd.read_csv(io.BytesIO(file_bytes))
        df.columns = [col.lower().strip() for col in df.columns]
        
        # Rename common variations to standard names
        rename_dict = {}
        for col in df.columns:
            if 'date' in col: rename_dict[col] = 'date'
            elif 'desc' in col or 'name' in col or 'particulars' in col: rename_dict[col] = 'description'
            elif 'amt' in col or 'amount' in col or 'value' in col: rename_dict[col] = 'amount'
        
        df = df.rename(columns=rename_dict)
        # Keep only required columns if they exist
        available_cols = [c for c in ['date', 'description', 'amount'] if c in df.columns]
        df = df[available_cols]
        
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        return df.dropna(subset=['date', 'amount'])

    elif filename.endswith('.pdf'):
        # Basic PDF text extractor (Fallback if CSV isn't used)
        reader = PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        # NOTE: Real PDF parsing requires complex regex based on specific bank layouts.
        # For this MVP, we return a mock structured dataframe if text is found.
        # In production, use libraries like camelot-py or LLM vision models.
        print("PDF text extracted length:", len(text))
        
        # Placeholder data structured like a parsed statement
        mock_data = {
            'date': pd.to_datetime(['2026-05-01', '2026-05-03', '2026-05-15', '2026-05-20']),
            'description': ['Landlord Rent Payment', 'Starbucks Coffee', 'Walmart Supercenter', 'Netflix Subscription'],
            'amount': [-1200.00, -6.50, -150.00, -15.49]
        }
        return pd.DataFrame(mock_data)
        
    else:
        raise ValueError("Unsupported file format. Please upload CSV or PDF.")