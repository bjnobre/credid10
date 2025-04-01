import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import re

def preprocess_image(image_path):
    """
    Preprocess the image to improve OCR accuracy.
    
    - If the image height is less than 1080 pixels, it is resized proportionally.
    - The image is then converted to grayscale.
    - Contrast is enhanced.
    - A median filter is applied for noise reduction.
    - Thresholding converts the image to pure black and white.
    - The processed image is shown for debugging purposes.
    
    Parameters:
        image_path (str): The path to the image file.
        
    Returns:
        Image: A preprocessed PIL Image object.
    """
    # Open the image
    img = Image.open(image_path)
    
    # Expand image if its height is less than 1080 pixels
    if img.height < 1080:
        scale_factor = 1080 / img.height
        new_width = int(img.width * scale_factor)
        new_height = 1080
        img = img.resize((new_width, new_height), resample=Image.LANCZOS)
    
    """
    # Convert to grayscale
    img = img.convert('L')
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)  # Increase contrast by a factor of 2
    
    # Apply a median filter to reduce noise
    img = img.filter(ImageFilter.MedianFilter())
    
    # Apply thresholding to convert the image to pure black and white
    threshold = 140
    img = img.point(lambda x: 0 if x < threshold else 255, '1')
    """
    
    # Display the processed image for analysis (for debugging)
    img.show(title="Processed Image")
    
    return img


def process_document(image_path):
    """
    Extracts text from a preprocessed image and attempts to process it as a salary receipt.
    If processing as a salary receipt fails, it falls back to processing as a bank account document.
    
    Parameters:
        image_path (str): The path to the image file.
        
    Returns:
        dict: A dictionary with the processed information.
    """
    # Enhance the image for better OCR accuracy
    enhanced_image = preprocess_image(image_path)

    # Use a custom configuration to set the page segmentation mode
    # --psm 6 treats the image as a single uniform block of text.
    custom_config = r'--psm 6'

    
    # Extract text from the enhanced image
    text = pytesseract.image_to_string(enhanced_image, config=custom_config, lang='por')
    
    try:
        # Attempt to process the text as a salary receipt
        return process_salary_receipt(text)
    except Exception as e:
        # If it fails, attempt to process it as a bank account document.
        return process_bankaccount_extract(text)

def process_salary_receipt(text):
    """
    Processes the OCR-extracted text to extract information from a salary receipt.
    
    The function first checks if the text contains the keywords "salário", "pagamento", and "recibo".
    If the check passes, it extracts key fields such as the gross salary, liquid salary, and document date.
    If not, it raises a ValueError.
    
    Parameters:
        text (str): The OCR-extracted text.
        
    Returns:
        dict: A dictionary containing extracted salary receipt information.
        
    Raises:
        ValueError: If the text does not appear to be from a salary receipt.
    """
    lower_text = text.lower()
    # Check for the presence of the required keywords
    if not all(word in lower_text for word in ["salário", "pagamento", "recibo"]):
        raise ValueError("O texto não parece ser de um recibo de pagamento de salário.")
    
    # Extract Gross Salary
    salary_match = re.search(r'Sal[aá]rio\s*Bruto[:\-]?\s*R\$\s*([\d\.,]+)', text, re.IGNORECASE)
    salario_bruto = salary_match.group(1).strip() if salary_match else None

    # Extract Liquid Salary
    liquid_match = re.search(r'Valor\s*L[ií]quido[:\-]?\s*R\$\s*([\d\.,]+)', text, re.IGNORECASE)
    valor_liquido = liquid_match.group(1).strip() if liquid_match else None

    # Extract Document Date (format DD/MM/YYYY)
    date_match = re.search(r'Data\s*[:\-]?\s*(\d{2}/\d{2}/\d{4})', text)
    data_documento = date_match.group(1).strip() if date_match else None

    return {
        "document_type": "salary_receipt",
        "salario_bruto": salario_bruto,
        "valor_liquido": valor_liquido,
        "data_documento": data_documento,
        "raw_text": text  # Optional, for debugging purposes
    }

def process_bankaccount_extract(text):
    """
    Processes the OCR-extracted text to extract information from a bank account document.
    
    This function is a placeholder and should be implemented to handle bank account extraction.
    
    Parameters:
        text (str): The OCR-extracted text.
        
    Returns:
        dict: A dictionary with bank account document information.
    """
    # Placeholder implementation: return a dummy response.
    return {
        "document_type": "bank_account",
        "info": "Função de extração bancária ainda não implementada.",
        "raw_text": text
    }
