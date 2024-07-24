---
cover_image: https://media.dev.to/cdn-cgi/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fk0euxhlzn6tr5ri7gfgv.png
created_at: 2022-02-18 15:04:48+00:00
description: We are pretty much familiar with the Typewriter effect, although we might
    not be acquainted with a...
edited_at: 2024-07-21 19:34:47+00:00
id: 993602
published: true
published_at: 2022-02-18 19:30:57+00:00
series: 17308
slug: designing-a-typewriter-react-component-3kea
tag_list: react, javascript, component
title: Designing a Typewriter React Component
---
We are pretty much familiar with the Typewriter effect, although we might not be acquainted with a Typewriter. In words, the typewriter effect is the gradual revealing of the words as if it is being typed infront of our eyes with sound of a typewriter key pressing. A popular Typewriter Animation in Web usually involves slowling revealing of the text with a blinking cursor and slowling erasing of the text with a pause.

Though in our today's exercise, we will be implementing a typewriter effect where a list of words are being typed on the screen with a blinking caret or cursor. After each word is being typed, it's also erased after a little pause to erase slowly one letter at a time and finally typed in for the next word.

## Getting Started

We won't require no extra libraries except the ones installed by *create-react-app* template.

**Typewriter.jsx**

```jsx
import React from 'react';

function Typewriter({ text, ...otherProps }) {
    return (
        <div className="Typewriter" {...otherProps}>
            <span className="Typewriter__text">{text}</span>
            <span className="Typewriter__cursor">|</span>
        </div>
    );
}

export default Typewriter;

```

A classic functional component that has **text** (string) prop for content and two child components, i.e., typewriter_text and typewriter_cursor. 

## Implementation

### Blinking caret

To design the blinking caret, we will need css into action.

Typewriter.css

```css
.Typewriter__text {
	display: inline-block;
}

.Typewriter__cursor {
	display: inline-block;
	color: currentColor;
    animation: blink 1s ease-in-out 0s infinite alternate;
}

@keyframes blink {
	from {
		opacity: 1;
	}
	to {
		opacity: 0;
	}
}
```

CSS3 Animations is used for blinking and both child components are made inline-block for making them side by side. Add a import in Typewriter jsx after React import

```jsx
import React from 'react';
import './Typewriter.css';

...
```



### Typing Effect

We will use two React Hooks namely useState and useEffect for this purpose.

```jsx
function Typewriter({ text, speed, ...otherProps }) {
    const [currentText, setCurrentText] = React.useState('');
    const [__timeout, set__Timeout] = React.useState(null);

    React.useEffect(() => {
        startTyping();

        return () => {
            __timeout && clearTimeout(__timeout);
        };
    }, []);

    React.useEffect(() => {
        let rawText = text;
        if (currentText.length < rawText.length) {
            set__Timeout(setTimeout(type, speed));
        }
        return () => {
            __timeout && clearTimeout(__timeout);
        };
    }, [currentText]);

    function startTyping() {
        set__Timeout(
            setTimeout(() => {
                type();
            }, speed)
        );
    }

    function type() {
        let rawText = text;

        if (currentText.length < rawText.length) {
            let displayText = rawText.substr(0, currentText.length + 1);
            setCurrentText(displayText);
        }
    }
    
	return (
		<div className="Typewriter" {...otherProps}>
			<span className="Typewriter__text">{currentText}</span>
			<span className="Typewriter__cursor">|</span>
		</div>
	);
}
```

The function **startTyping** initiates the first call for text change. The function **type** updates the current text while on every update of **currentText**, type function is called after every **speed** (which is passed as a prop) milliseconds. 

### Erasing Effect

We have already implemented the typing effect, and for erasing effect, we need a flag to know whether we are typing or erasing. Thereby, we can create a cycle of typing to erasing and vice-versa.

```jsx
function Typewriter({ text, speed, eraseSpeed, typingDelay, eraseDelay, ...otherProps }) {
    ...
	const [isTyping, setIsTyping] = React.useState(true);
    
    ...
    
    React.useEffect(() => {
		let rawText = text;
		if (isTyping) {
			if (currentText.length < rawText.length) {
				set__Timeout(setTimeout(type, speed));
			} else {
				setIsTyping(false);
				set__Timeout(setTimeout(erase, eraseDelay));
			}
		} else {
			if (currentText.length === 0) {
				setIsTyping(true);
				setTimeout(startTyping, typingDelay);
			} else {
				set__Timeout(setTimeout(erase, eraseSpeed));
			}
		}
		return () => {
			__timeout && clearTimeout(__timeout);
		};
	}, [currentText]);
    
    ...
    
    function erase() {
		if (currentText.length !== 0) {
			let displayText = currentText.substr(-currentText.length, currentText.length - 1);
			setCurrentText(displayText);
		}
	}
    
    ...
    
}
```

Added an **erase** function for diminishing effect and a state variable **isTyping** for erasing or typing switch. Updated the useEffect on currentText for startTyping when currentText.length is zero with **typingDelay** (added to the props) seconds and switch to typing, else erase is called after every **eraseSpeed** (added to the props) milliseconds. For typing mode, added switch to erasing after **erasingDelay** when currentText.length reaches full length.

### Enabling Array of Text

We need to add an index for the array and function to handle array or string for text prop.

```jsx
function Typewriter({ text, speed, eraseSpeed, typingDelay, eraseDelay, ...otherProps }) {
    ...
	const [currentIndex, setCurrentIndex] = React.useState(0);
    
    ...
    React.useEffect(() => {
		let rawText = getRawText()[currentIndex];
		if (isTyping) {
        ...
        } else {
			if (currentText.length === 0) {
				const textArray = getRawText();
				let index = currentIndex + 1 === textArray.length ? 0 : currentIndex + 1;
				if (index === currentIndex) {
					setIsTyping(true);
					setTimeout(startTyping, typingDelay);
				} else {
					setTimeout(() => setCurrentIndex(index), typingDelay);
				} 
            }
            else {
				set__Timeout(setTimeout(erase, eraseSpeed));
			}
        }
        ...
	}, [currentText]);   
            
    
	React.useEffect(() => {
		if (!isTyping) {
			setIsTyping(true);
			startTyping();
		}
		return () => {
			__timeout && clearTimeout(__timeout);
		};
	}, [currentIndex]);

	function getRawText() {
		return typeof text === 'string' ? [text] : [...text];
	}
    
    ...
	function type() {
		let rawText = getRawText()[currentIndex];
        ...
    }
    
    function erase() {
		let index = currentIndex;
		if (currentText.length !== 0) {
			let displayText = currentText.substr(-currentText.length, currentText.length - 1);
			setCurrentText(displayText);
		} else {
			const textArray = getRawText();
			index = index + 1 === textArray.length ? 0 : index + 1;
			setCurrentIndex(index);
		}
	}
    
    ...
}
    
```

Added **getRawText** function to handle string or array at the same time from text prop and added state variable **currentIndex** for array index. Updated useEffect for currentText, in erasing mode, to switch to next string in array and start typing. Added useEffect for currentIndex, to setTyping true and startTyping.

### Alternate cursor

```jsx
...
function Typewriter({ text, speed, eraseSpeed, cursor, typingDelay, eraseDelay, ...otherProps }) {
    ...
    return (
		<div className="Typewriter" {...otherProps}>
			<span className="Typewriter__text">{currentText}</span>
			<span className="Typewriter__cursor">{cursor}</span>
		</div>
	);
}
```

Added **cursor** to the prop and added the same in return section of the function

### Adding PropTypes and default Props

Added import for proptypes

```jsx
import React from 'react';
import PropTypes from 'prop-types';
import './Typewriter.css';
...
```

Added defaultProps for speed, eraseSpeed, typingDelay and eraseDelay

```jsx
Typewriter.propTypes = {
	speed: PropTypes.number.isRequired,
	eraseSpeed: PropTypes.number.isRequired,
	typingDelay: PropTypes.number.isRequired,
	eraseDelay: PropTypes.number.isRequired,
	cursor: PropTypes.string,
	text: PropTypes.oneOfType([PropTypes.arrayOf(PropTypes.string), PropTypes.string]).isRequired,
};

Typewriter.defaultProps = {
	speed: 500,
	eraseSpeed: 400,
	typingDelay: 2500,
	eraseDelay: 5000,
};
```

## Final Code

Final Code for Typewriter.jsx

<https://github.com/shivishbrahma/nuclear-reactor/blob/main/src/Typewriter/Typewriter.jsx>

## Use withtin App Component

```jsx
import './App.css';
import Typewriter from './Typewriter';

function App() {
	return <div className="App">
        <Typewriter text={["Typewriter Effect", "A React Component"]}/>
    </div>;
}

export default App;
```

## Preview

![Preview of Typewriter](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/8sg8lmx0i84dnwt62wlr.gif)
 

## References

- [TypewriterJS](https://www.npmjs.com/package/typewriter-effect)
- [React-typewriter-effect](https://www.npmjs.com/package/react-typewriter-effect) 
- [Typewriter Effect - CSS Tricks](https://css-tricks.com/snippets/css/typewriter-effect/)