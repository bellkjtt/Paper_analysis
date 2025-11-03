# Paper Analysis Frontend

Modern Next.js web application for academic paper analysis with AI-powered insights.

## Features

- **PDF Upload**: Drag-and-drop or click to upload academic papers
- **Real-time Progress**: Live progress tracking during analysis
- **Beautiful Rendering**: Markdown-based display with syntax highlighting
- **Export Options**: Download as Markdown or PDF
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **TypeScript**: Full type safety
- **Modern UI**: Built with Tailwind CSS

## Tech Stack

- **Next.js 15**: React framework with App Router
- **React 18**: Modern React with hooks
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **react-markdown**: Markdown rendering
- **jsPDF + html2canvas**: PDF export functionality

## Prerequisites

- Node.js 18 or higher
- npm or yarn package manager
- Running backend API (see main README)

## Installation

1. Navigate to the frontend directory:
```bash
cd paper-analysis-next
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment variables:
```bash
cp .env.local.example .env.local
```

4. Edit `.env.local` with your backend URL:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Development

Start the development server:

```bash
npm run dev
```

The application will be available at http://localhost:3000

### Development Features

- Hot reload on file changes
- Fast refresh for React components
- TypeScript error checking
- ESLint integration

## Build

Build for production:

```bash
npm run build
```

This will create an optimized production build in the `.next` folder.

## Production

Run the production server:

```bash
npm start
```

The server will listen on `0.0.0.0:3000` for network access.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8000` |

**Note**: All client-side environment variables must be prefixed with `NEXT_PUBLIC_`.

## Project Structure

```
app/
├── page.tsx          # Main analysis page
├── layout.tsx        # Root layout with metadata
└── globals.css       # Global styles and Tailwind imports

lib/
├── api.ts            # API client for backend communication
├── markdown-utils.ts # Markdown processing utilities
└── pdf-utils.ts      # PDF export utilities

types/
└── index.ts          # TypeScript type definitions
```

## Usage

1. **Start backend**: Make sure the backend API is running on port 8000
2. **Open app**: Navigate to http://localhost:3000
3. **Upload PDF**: Click "PDF 파일 선택" or drag and drop a PDF file
4. **Analyze**: Click "분석 시작" to begin analysis
5. **View Results**: Wait for the analysis to complete (≈12 seconds per page)
6. **Download**: Export as Markdown or PDF

## Features in Detail

### PDF Upload

- Max file size: 50MB
- Accepted format: PDF only
- Validation: File type and size checking
- User feedback: Clear error messages

### Progress Tracking

- Real-time progress updates
- Stage indicators: Extracting → Analyzing → Finalizing
- Page-by-page progress display
- Estimated time remaining

### Markdown Rendering

- Syntax highlighting for code blocks
- Proper heading hierarchy
- Link formatting
- Table support
- Image embedding (if present)

### Export Features

#### Markdown Download
- Plain text markdown file
- Preserves all formatting
- Includes embedded images as base64

#### PDF Download
- Formatted PDF with styling
- Preserves layout and formatting
- Generated client-side
- No backend dependency

## Development Tips

### Type Checking

```bash
npx tsc --noEmit
```

### Linting

```bash
npm run lint
```

### Clean Build

```bash
rm -rf .next node_modules
npm install
npm run build
```

## Deployment

### Vercel (Recommended)

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Deploy:
```bash
vercel --prod
```

3. Set environment variables in Vercel dashboard:
   - `NEXT_PUBLIC_API_URL`: Your backend API URL

### Other Platforms

Build and deploy the production files:

```bash
npm run build
```

Upload the `.next`, `public`, and `package.json` files to your hosting platform.

## Troubleshooting

### Cannot connect to backend

**Symptoms**: "Failed to fetch" errors

**Solutions**:
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check `NEXT_PUBLIC_API_URL` in `.env.local`
3. Restart dev server after changing environment variables
4. Check CORS settings on backend

### Build failures

**Symptoms**: `npm run build` fails

**Solutions**:
1. Clear cache: `rm -rf .next`
2. Reinstall dependencies: `rm -rf node_modules && npm install`
3. Check Node.js version: `node --version` (requires 18+)
4. Check TypeScript errors: `npx tsc --noEmit`

### Environment variables not loading

**Solutions**:
1. Ensure variables start with `NEXT_PUBLIC_`
2. Restart dev server after changing `.env.local`
3. Don't use `.env` for Next.js, use `.env.local`
4. Clear Next.js cache: `rm -rf .next`

### PDF export not working

**Solutions**:
1. Check browser console for errors
2. Ensure `jspdf` and `html2canvas` are installed
3. Try disabling browser extensions
4. Use a modern browser (Chrome, Firefox, Safari, Edge)

## Browser Support

- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions
- Mobile browsers: iOS Safari, Chrome Mobile

## Performance

- Initial load: < 2 seconds
- Time to Interactive: < 3 seconds
- Lighthouse score: 90+
- Bundle size: < 500KB (gzipped)

## Security

- Environment variables for API URLs
- No sensitive data in client-side code
- Input validation for file uploads
- XSS protection via React
- HTTPS recommended for production

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Run linting: `npm run lint`
5. Build: `npm run build`
6. Submit a pull request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](../LICENSE) file for details.

## Support

For issues specific to the frontend:
- Check browser console for errors
- Verify backend is accessible
- Review environment variables
- Check the main [README](../README.md) for full stack setup

---

**Need help?** Open an issue on GitHub with:
- Browser and version
- Error messages
- Steps to reproduce
- Screenshots (if applicable)
