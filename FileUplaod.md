# iQuiz
SWE 444 project
Implementing functionality to accept and process various file formats such as PDF, DOCX, and PPTX, then convert them into a standardized format like JSON or HTML for further manipulation and extraction is a multi-step process. Here's a simplified breakdown of how you could approach this challenge for your iQuiz project:

1. **File Upload System**:
   - Implement a file upload system on your website where users can upload their documents.
   - You can use HTML `<input type="file">` element for file uploading, and backend frameworks like Flask or Django if your website is based on Python, or Express.js if it's based on Node.js, to handle file uploads.

2. **File Validation**:
   - Verify that the uploaded files are of the supported formats (PDF, DOCX, PPTX) to prevent any processing errors.
   - This can be done by checking the file extension or using a library to inspect the file's format.

3. **File Conversion**:
   - Convert the uploaded files into a standardized intermediate format like HTML or plain text, which will make it easier to further process and extract information.
   - For PDFs, libraries like PyMuPDF or Apache PDFBox can be used.
   - For DOCX, libraries like python-docx or Apache POI can be used.
   - For PPTX, Apache POI or python-pptx can be used.

4. **Information Extraction**:
   - Extract information, summaries, and potential quiz questions from the standardized format.
   - You can use Natural Language Processing (NLP) libraries like spaCy or NLTK for text analysis and extraction.

5. **Conversion to JSON**:
   - Convert the extracted information into a structured JSON format which can then be manipulated or displayed on your website.
   - JSON is a lightweight data interchange format and is easy to read and write.

6. **Display on Website**:
   - Use the generated JSON to display summaries and quizzes on your website.
   - You can use frontend libraries like React or Angular to render the JSON data on your website.

7. **Additional Considerations**:
   - It may be beneficial to consider an asynchronous processing model, especially if file conversion and processing may take some time. This way, you can notify users once their summaries and quizzes are ready.
   - Ensuring data privacy and security is crucial, especially when dealing with user-uploaded files. Make sure to follow best practices to protect user data.

By following this general outline, modifying as necessary to fit the specific needs and technologies of your project, you should be well on your way to implementing the desired functionality for iQuiz. This project will likely require a combination of frontend and backend development, along with a good understanding of file processing and NLP techniques.


# Libraries

### 1. PDF Processing:
- **Python**:
  - PyMuPDF
  - PyPDF2
  - pdfminer.six

- **Java**:
  - Apache PDFBox
  - iText

- **JavaScript/Node.js**:
  - pdf-lib
  - pdf2pic
  - hummusJS

- **Ruby**:
  - PDF::Reader
  - CombinePDF

- **C#**:
  - iTextSharp
  - PdfPig

### 2. DOCX Processing:
- **Python**:
  - python-docx
  - docx2txt

- **Java**:
  - Apache POI
  - docx4j

- **JavaScript/Node.js**:
  - mammoth.js
  - docxtemplater

- **Ruby**:
  - ruby-docx
  - docx_replace

- **C#**:
  - DocX
  - OpenXML SDK

### 3. PPTX Processing:
- **Python**:
  - python-pptx
  - pptx2pdf

- **Java**:
  - Apache POI
  - pptx4j (part of docx4j)

- **JavaScript/Node.js**:
  - pptxgenjs
  - officegen

- **Ruby**:
  - powerpoint (gem)
  - rslide (gem)

- **C#**:
  - OpenXML SDK
  - Spire.Presentation

### 4. Conversion to HTML/Text/JSON:
- **Python**:
  - Beautiful Soup (for HTML parsing)
  - json (standard library for JSON)

- **Java**:
  - Jsoup (for HTML parsing)
  - Jackson (for JSON)

- **JavaScript/Node.js**:
  - cheerio (for HTML parsing)
  - JSON.parse() and JSON.stringify() (for JSON)

- **Ruby**:
  - Nokogiri (for HTML parsing)
  - JSON (standard library for JSON)

- **C#**:
  - HtmlAgilityPack (for HTML parsing)
  - Newtonsoft.Json (for JSON)

These libraries can help you manipulate and convert file formats as per the requirements of your iQuiz project. You may need to explore the documentation and community resources related to these libraries to understand their capabilities and limitations.
