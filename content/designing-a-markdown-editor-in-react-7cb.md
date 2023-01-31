---
cover_image: https://res.cloudinary.com/practicaldev/image/fetch/s--5fJxFgxf--/c_imagga_scale,f_auto,fl_progressive,h_420,q_auto,w_1000/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/kt7jmjn0lxpbfp867imd.png
description: Ever since the popularity of open-source libraries, Markdown has always
  been the primary text format...
id: 1022617
published: true
published_at: '2022-03-14T18:36:08.961Z'
tags:
- javascript
- webdev
- markdown
- component
title: Designing a Markdown Editor in React
---
Ever since the popularity of open-source libraries, Markdown has always been the primary text format for documentation of these libraries after txt. Since Markdown supports word processing like formatting along with text like script, it is more readable and can easily formatted to a HTML script for web rendering. By the recent updates, Github has standardised many other formatting syntaxes to  support more HTML like features into markdown.

In this blog, we will be designing a react component that parses markdown content to convert into HTML code for rendering as preview.

## Getting Started

Starting with create-react-app template, we need to install `markdown-it` library for markdown to html conversion.

**MarkdownEditor.jsx**

```jsx
import React from 'react';

export default function MarkdownEditor() {
	return (
		<div className="MarkdownEditor">
			<div className="MarkdownEditor__Editor"></div>
			<div className="MarkdownEditor__Preview"></div>
		</div>
	);
}
```

This functional component MarkdownEditor has two tabs for markdown input, i.e., Editor and for html output, i.e., Preview. 

## Implementation

### Basic Tab Components

We add a textarea for the Editor component and a html div for Preview component and also a titleBar for each.

**MarkdownEditor.jsx**

```jsx
...
export default function MarkdownEditor({ content: contentProps }) {
	const [content, setContent] = React.useState(contentProps);
	function handleChange(evt) {
		console.log(evt.target.value);
		setContent(evt.target.value);
	}
	return (
		<div className="MarkdownEditor">
			<div className="MarkdownEditor__Editor">
				<div className="titleBar">Editor</div>
				<textarea className="MarkdownEditor__Editor__Textarea" value={content} onChange={(evt)=>handleChange(evt)} />
			</div>
			<div className="MarkdownEditor__Preview">
				<div className="titleBar">Preview</div>
				<div className="MarkdownEditor__Preview__Content"></div>
			</div>
		</div>
	);
}
```

Adding a onChange handler function for the textarea value change and content props is passed for pre-initialization.

### Adding Styles

Styling both the tabs for editor with preview mode view.

**MarkdownEditor.css**

```css
.MarkdownEditor {
	display: flex;
	height: 100%;
	width: 100%;
	overflow: hidden;
}

.MarkdownEditor__Editor,
.MarkdownEditor__Preview {
	flex: 1;
}

.MarkdownEditor .titleBar {
	width: 100%;
	height: 3rem;
	padding: 0.5rem;
    display: flex;
    align-items: center;
	background-color: #391a42;
	color: #fff;
}

.MarkdownEditor__Editor__Textarea {
	width: calc(100% - 1.25rem);
	height: calc(100% - 5rem);
	border: none;
	resize: none;
	padding: 0.5rem;
	background-color: #57659c;
	color: #fff;
	font-family: 'Tlw Typewriter', 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
	font-size: 1rem;
	line-height: 1.5;
	overflow: auto;
}

.MarkdownEditor__Preview__Content {
	width: calc(100% - 1.25rem);
	height: calc(100% - 5rem);
	padding: 0.5rem;
	font-family: 'Tlw Typewriter', 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
	font-size: 1rem;
	line-height: 1.5;
	overflow: auto;
}
```

### Using Markdown-It

Installing markdown-it

```bash
npm i markdown-it
```

**MarkdownEditor.jsx**

```jsx
...
import markdownIt from 'markdown-it';
import './MarkdownEditor.css';

export default function MarkdownEditor({ content: contentProps }) {
	...
	function toMarkdown(content) {
		const md = markdownIt({
			html: true,
			linkify: true,
			typographer: true,
		});
		return md.render(content);
	}
	return (
		<div className="MarkdownEditor">
			...
			<div className="MarkdownEditor__Preview">
                ...
				<div
					className="MarkdownEditor__Preview__Content"
					dangerouslySetInnerHTML={{ __html: toMarkdown(content) }}
				></div>
			</div>
		</div>
	);
}
```

We use dangerouslySetInnerHTML for setting html content for the Preview Component and define a function toMarkdown to convert markdown content into HTML.

### Adding Fullscreen

```jsx
...
export default function MarkdownEditor({ content: contentProps }) {
    ...
	const [editorMaximized, setEditorMaximized] = React.useState(false);
	const [previewMaximized, setPreviewMaximized] = React.useState(false);
    ...
    
	function handleEditorMaximize() {
		if (!previewMaximized) setEditorMaximized(!editorMaximized);
		else setPreviewMaximized(false);
	}
	function handlePreviewMaximize() {
		if (!editorMaximized) setPreviewMaximized(!previewMaximized);
		else setEditorMaximized(false);
	}
    
	return (
		<div className="MarkdownEditor">
			{previewMaximized ? (
				<></>
			) : (
				<div className="MarkdownEditor__Editor">
					<div className="titleBar">
						Editor
						<div style={{ marginLeft: 'auto' }} onClick={handleEditorMaximize}>
							{editorMaximized ? <span>-&gt;&lt;-</span> : <span>&lt;--&gt;</span>}
						</div>
					</div>
					<textarea
						className="MarkdownEditor__Editor__Textarea"
						value={content}
						onChange={(evt) => handleChange(evt)}
					/>
				</div>
			)}

			{editorMaximized ? (
				<></>
			) : (
				<div className="MarkdownEditor__Preview">
					<div className="titleBar">
						Preview
						<div style={{ marginLeft: 'auto' }} onClick={handlePreviewMaximize}>
							{previewMaximized ? <span>-&gt;&lt;-</span> : <span>&lt;--&gt;</span>}
						</div>
					</div>
					<div
						className="MarkdownEditor__Preview__Content"
						dangerouslySetInnerHTML={{ __html: toMarkdown(content) }}
					></div>
				</div>
			)}
		</div>
	);
}
```

Having two states editorMaximized and previewMaximized, for toggling of the editor and preview maximize with two functions as handlers for click.

## Final Code

**MarkdownEditor.css**

<https://github.com/shivishbrahma/nuclear-reactor/blob/main/src/MarkdownEditor/MarkdownEditor.css>

**MarkdownEditor.jsx**

<https://github.com/shivishbrahma/nuclear-reactor/blob/main/src/MarkdownEditor/MarkdownEditor.jsx>

## Preview

![Markdown Editor Preview](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/mez0xskwqmhcvy48fukq.png)

## Reference

-   [React Markdown Editor](https://github.com/rexxars/react-markdown)
