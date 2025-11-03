/**
 * Simple Markdown Renderer
 * Converts markdown text to HTML
 * Single Responsibility: Markdown parsing only
 */

const MarkdownRenderer = {
    /**
     * Convert markdown to HTML
     * @param {string} markdown - Markdown text
     * @returns {string} HTML string
     */
    render(markdown) {
        if (!markdown) {
            return '';
        }

        let html = markdown;

        // Escape HTML to prevent XSS
        html = this._escapeHtml(html);

        // Process in order: blocks first, then inline
        html = this._processCodeBlocks(html);
        html = this._processHeadings(html);
        html = this._processLists(html);
        html = this._processBlockquotes(html);
        html = this._processParagraphs(html);

        // Inline elements
        html = this._processInlineCode(html);
        html = this._processBold(html);
        html = this._processItalic(html);
        html = this._processImages(html);
        html = this._processLinks(html);

        return html;
    },

    /**
     * Escape HTML special characters
     */
    _escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    },

    /**
     * Process code blocks (```)
     */
    _processCodeBlocks(text) {
        return text.replace(
            /```([\s\S]*?)```/g,
            '<pre><code>$1</code></pre>'
        );
    },

    /**
     * Process headings (# ## ###)
     */
    _processHeadings(text) {
        const lines = text.split('\n');
        const processed = lines.map(line => {
            if (line.startsWith('#### ')) {
                return `<h4>${line.substring(5)}</h4>`;
            }
            if (line.startsWith('### ')) {
                return `<h3>${line.substring(4)}</h3>`;
            }
            if (line.startsWith('## ')) {
                return `<h2>${line.substring(3)}</h2>`;
            }
            if (line.startsWith('# ')) {
                return `<h1>${line.substring(2)}</h1>`;
            }
            return line;
        });
        return processed.join('\n');
    },

    /**
     * Process lists (- or 1.)
     */
    _processLists(text) {
        const lines = text.split('\n');
        const processed = [];
        let inList = false;
        let listType = null;

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            const isUnorderedItem = line.match(/^[-*]\s+(.+)/);
            const isOrderedItem = line.match(/^\d+\.\s+(.+)/);

            if (isUnorderedItem) {
                if (!inList || listType !== 'ul') {
                    if (inList) processed.push(`</${listType}>`);
                    processed.push('<ul>');
                    listType = 'ul';
                    inList = true;
                }
                processed.push(`<li>${isUnorderedItem[1]}</li>`);
            } else if (isOrderedItem) {
                if (!inList || listType !== 'ol') {
                    if (inList) processed.push(`</${listType}>`);
                    processed.push('<ol>');
                    listType = 'ol';
                    inList = true;
                }
                processed.push(`<li>${isOrderedItem[1]}</li>`);
            } else {
                if (inList) {
                    processed.push(`</${listType}>`);
                    inList = false;
                    listType = null;
                }
                processed.push(line);
            }
        }

        if (inList) {
            processed.push(`</${listType}>`);
        }

        return processed.join('\n');
    },

    /**
     * Process blockquotes (>)
     */
    _processBlockquotes(text) {
        return text.replace(
            /^>\s+(.+)$/gm,
            '<blockquote>$1</blockquote>'
        );
    },

    /**
     * Process paragraphs
     */
    _processParagraphs(text) {
        const lines = text.split('\n');
        const processed = [];
        let inParagraph = false;
        let paragraphLines = [];

        for (const line of lines) {
            const trimmed = line.trim();

            // Skip if already processed (HTML tags)
            if (trimmed.startsWith('<')) {
                if (inParagraph) {
                    processed.push(`<p>${paragraphLines.join(' ')}</p>`);
                    paragraphLines = [];
                    inParagraph = false;
                }
                processed.push(line);
                continue;
            }

            // Empty line ends paragraph
            if (trimmed === '') {
                if (inParagraph) {
                    processed.push(`<p>${paragraphLines.join(' ')}</p>`);
                    paragraphLines = [];
                    inParagraph = false;
                }
                processed.push('');
                continue;
            }

            // Add to paragraph
            paragraphLines.push(trimmed);
            inParagraph = true;
        }

        // Close final paragraph
        if (inParagraph) {
            processed.push(`<p>${paragraphLines.join(' ')}</p>`);
        }

        return processed.join('\n');
    },

    /**
     * Process inline code (`)
     */
    _processInlineCode(text) {
        return text.replace(
            /`([^`]+)`/g,
            '<code>$1</code>'
        );
    },

    /**
     * Process bold text (**)
     */
    _processBold(text) {
        return text.replace(
            /\*\*([^\*]+)\*\*/g,
            '<strong>$1</strong>'
        );
    },

    /**
     * Process italic text (*)
     */
    _processItalic(text) {
        return text.replace(
            /\*([^\*]+)\*/g,
            '<em>$1</em>'
        );
    },

    /**
     * Process images (![alt](url))
     */
    _processImages(text) {
        const API_BASE_URL = 'http://127.0.0.1:8000';

        return text.replace(
            /!\[([^\]]*)\]\(([^\)]+)\)/g,
            (match, alt, url) => {
                // Add API base URL if it's a relative path
                const fullUrl = url.startsWith('/') ? `${API_BASE_URL}${url}` : url;
                return `<img src="${fullUrl}" alt="${alt}" style="max-width: 100%; height: auto; margin: 1rem 0; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">`;
            }
        );
    },

    /**
     * Process links ([text](url))
     */
    _processLinks(text) {
        return text.replace(
            /\[([^\]]+)\]\(([^\)]+)\)/g,
            '<a href="$2" target="_blank" rel="noopener">$1</a>'
        );
    }
};
