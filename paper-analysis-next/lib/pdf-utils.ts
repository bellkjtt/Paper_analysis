/**
 * PDF conversion utilities
 */

/**
 * Convert HTML element to PDF
 * This is a client-side PDF generator that requires jsPDF and html2canvas
 * @param element HTML element to convert
 * @param filename PDF filename
 */
export async function convertToPDF(element: HTMLElement, filename: string): Promise<void> {
  try {
    // Dynamic import to reduce bundle size
    const [{ default: html2canvas }, { default: jsPDF }] = await Promise.all([
      import('html2canvas'),
      import('jspdf'),
    ]);

    // Convert HTML to canvas
    const canvas = await html2canvas(element, {
      scale: 2, // Higher quality
      useCORS: true, // Enable CORS for images
      logging: false,
      backgroundColor: '#ffffff',
    });

    const imgData = canvas.toDataURL('image/png');
    const imgWidth = 210; // A4 width in mm
    const pageHeight = 297; // A4 height in mm
    const imgHeight = (canvas.height * imgWidth) / canvas.width;
    let heightLeft = imgHeight;

    const pdf = new jsPDF('p', 'mm', 'a4');
    let position = 0;

    // Add first page
    pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
    heightLeft -= pageHeight;

    // Add additional pages if content is longer than one page
    while (heightLeft > 0) {
      position = heightLeft - imgHeight;
      pdf.addPage();
      pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
      heightLeft -= pageHeight;
    }

    // Save PDF
    pdf.save(filename);
  } catch (error) {
    console.error('Error converting to PDF:', error);
    throw new Error('PDF 변환에 실패했습니다.');
  }
}

/**
 * Alternative: Convert markdown content to PDF using a simpler approach
 * This creates a temporary div, renders the markdown, and converts to PDF
 * @param markdownHtml Rendered HTML from markdown
 * @param filename PDF filename
 */
export async function markdownToPDF(markdownHtml: string, filename: string): Promise<void> {
  // Create temporary container
  const container = document.createElement('div');
  container.style.position = 'absolute';
  container.style.left = '-9999px';
  container.style.width = '794px'; // A4 width in pixels at 96 DPI
  container.style.padding = '40px';
  container.style.backgroundColor = '#ffffff';
  container.innerHTML = markdownHtml;

  // Add Tailwind prose classes for styling
  container.classList.add('prose', 'prose-gray', 'max-w-none');

  document.body.appendChild(container);

  try {
    await convertToPDF(container, filename);
  } finally {
    document.body.removeChild(container);
  }
}
