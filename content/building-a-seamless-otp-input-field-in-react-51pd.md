---
cover_image: https://media.dev.to/cdn-cgi/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fhsostoqsrl16ixfm4lss.png
created_at: 2024-07-27 17:25:05+00:00
description: In today's digital age, ensuring secure access to online services is
    paramount, and One-Time...
edited_at: 2024-07-28 13:10:37+00:00
id: 1938435
published: true
published_at: 2024-07-27 17:25:05+00:00
series: 17308
slug: building-a-seamless-otp-input-field-in-react-51pd
tags:
- react
- javascript
- webdev
- component
title: 'Building a Seamless OTP Input Field in React: A Step-by-Step Guide'
---
In today's digital age, ensuring secure access to online services is paramount, and One-Time Passwords (OTPs) play a crucial role in this process. OTPs provide an additional layer of security by requiring users to enter a unique code sent to their mobile device or email. Implementing an OTP input field that is both user-friendly and secure can significantly enhance the user experience of your application.

In this step-by-step guide, we will walk you through the process of building a seamless OTP input field in React. We will cover essential features such as automatically moving to the next input box upon entering a digit, handling backspace for deleting digits, navigating between input fields with arrow keys, and efficiently handling paste operations. By the end of this tutorial, you will have a robust OTP input component ready to integrate into your React application, ensuring a smooth and intuitive user experience for your users.

## Getting Started

Starting with the basic cra-template of *create-react* app

**OTPInput.jsx**

```jsx
import React from 'react'
import PropTypes from 'prop-types'

function OTPInput({...otherProps}) {
  return (
    <div className="OTPInput" {...otherProps}></div>
  );
}

OTPInput.propTypes = {};

export default OTPInput;
```

A simple functional component with **otherProps**.

## Implementation

### Input Fields for Each Digit

We will add input fields for each digit in the OTP using **length** prop spreading over list of numbers from 1 to **length** . A shortcut to generate numbers from 1 to **length** is `Array(length).fill(i + 1)`.

```jsx
...
function OTPInput({length, ...otherProps}) {
    const [otp, setOtp] = React.useState("");
    const inputs = [];
    
    return (
        <div className="OTPInput" {...otherProps}>
            {Array(length)
                .fill((_, i) => i + 1)
                .map((_, index) => (
                    <input
                        className="OTPInput__input"
                        key={index}
                        type="text"
                        maxLength="1"
                        value={otp[index]?.toString() || ""}
                        placeholder="0"
                        ref={(input) => (inputs[index] = input)}
                    />
                ))}
        </div>    
    );
}

OTPInput.propTypes = {
    length: PropTypes.number
};

OTPInput.defaultProps = {
    length: 6
};
...
```

Introducing a state for **otp** and a **setOtp** function to update the state. We will use **otp** to store the current OTP value and **setOtp** to update the state. Each input element value is indexed over this state variable. The **inputs** array will be used to store the input elements used to render the OTP. The **length** prop is used to determine the number of input fields to render and is set to 6 by default.

### Styling OTP Inputs

**OTPInput.css**

```css
.OTPInput__input {
    width: 40px;
    height: 40px;
    text-align: center;
    margin: 0 5px;
    font-size: 20px;
}
```

```jsx
...
import './OTPInput.css';
...
```

The *OTPInput__input* class is used to style the input elements.

### Handling Input

```jsx
...
function OTPInput({length, pattern, ...otherProps}) {
    ...

    const handleChange = (element, index) => {
        const value = element.value;
        if (!pattern.test(value)) return; // Only allow digits

        let newOtp = [...otp];
        newOtp[index] = value;

        setOtp(newOtp);

        // Move to the next input field
        if (value && index < length - 1) {
            inputs[index + 1].focus();
        }
    };

    return (
        <div className="OTPInput" {...otherProps}>
            {Array(length)
                .fill((_, i) => i + 1)
                .map((_, index) => (
                    <input
                        className="OTPInput__input"
                        key={index}
                        type="text"
                        maxLength="1"
                        value={otp[index]?.toString() || ""}
                        onChange={(e) => handleChange(e.target, index)}
                        placeholder="0"
                        ref={(input) => (inputs[index] = input)}
                    />
                ))}
        </div>
    );
}

OTPInput.propTypes = {
    ...
    pattern: PropTypes.instanceOf(RegExp)
};

OTPInput.defaultProps = {
    ...
    pattern: /\d/
};
...
```

The **pattern** prop is used to validate the input value, which is set to `/\d/` by default. The function *handleChange* updates the **otp** state with the new value, avoids the change if it doesn't match the pattern, also sets the focus to the next input field.

### Handling Paste

```jsx
...
function OTPInput({length, pattern, ...otherProps}) {
    ...
    const handlePaste = (e) => {
        e.preventDefault();
        const paste = e.clipboardData.getData("text");
        if (!pattern.test(paste)) return; // Only allow digits

        const newOtp = paste.slice(0, length).split("");
        for (let i = 0; i < length; i++) {
            inputs[i].value = newOtp[i] || "";

            if (newOtp[i] && i < length - 1) {
                inputs[i + 1].focus();
            }
        }
        setOtp(newOtp);
    };

    return (
        <div className="OTPInput" {...otherProps} onPaste={handlePaste}>
            {Array(length)
                .fill((_, i) => i + 1)
                .map((_, index) => (
                    <input
                        className="OTPInput__input"
                        key={index}
                        type="text"
                        maxLength="1"
                        value={otp[index]?.toString() || ""}
                        onChange={(e) => handleChange(e.target, index)}
                        placeholder="0"
                        ref={(input) => (inputs[index] = input)}
                    />
                ))}
        </div>
    );
}
...
```

The function *handlePaste* matches the pasted value with the **pattern**, updates the **otp** state from the pasted value and sets the focus to the next empty input field. The paste function is set to the whole OTPInput component.

### Deleting Values and Moving Focus

```jsx
...
function OTPInput({length, pattern, ...otherProps}) {
    ...

    const handleKeyDown = (e, index) => {
        if (e.key === "Backspace") {
            e.preventDefault();
            let newOtp = [...otp];
            newOtp[index] = "";
            setOtp(newOtp);

            if (index > 0) {
                inputs[index - 1].focus();
            }
        } else if (e.key === "ArrowLeft" && index > 0) {
            inputs[index - 1].focus();
        } else if (e.key === "ArrowRight" && index < length - 1) {
            inputs[index + 1].focus();
        }
    };
    ...

    return (
        <div className="OTPInput" {...otherProps} onPaste={handlePaste}>
            {Array(length)
                .fill((_, i) => i + 1)
                .map((_, index) => (
                    <input
                        className="OTPInput__input"
                        key={index}
                        type="text"
                        maxLength="1"
                        value={otp[index]?.toString() || ""}
                        onChange={(e) => handleChange(e.target, index)}
                        onKeyDown={(e) => handleKeyDown(e, index)}
                        placeholder="0"
                        ref={(input) => (inputs[index] = input)}
                    />
                ))}
        </div>
    );
}
...
```

The function *handleKeyDown* is used for keypress events. For deletion via **backspace**, the function sets the focus to the previous input field and removes the value of the current input field. For moving focus via arrow keys, the function sets the focus to the next / previous input field.

## Final Code

**OTPInput.jsx**

<https://github.com/shivishbrahma/nuclear-reactor/blob/main/src/OTPInput/OTPInput.jsx>

## Use within App component

```jsx
import OTPInput from './OTPInput';
import './App.css';

function App() {
    return (
        <div className="App">
            <OTPInput />
        </div>
    )
}

export default App;
```

## Preview

> OTPInput Preview

![OTPInput Preview](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/d9fvtbyuh91eaz7aad3q.gif)

> Traversing through OTPInput Preview

![Traversing through OTPInput Preview](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/b6u3jwvl1t6geoqlt8r6.gif)

> Copy Paste in OTPInput Preview

![Copy Paste in OTPInput Preview](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/f10bybu05zq0ao6rvc89.gif)

## References

- [ClipboardEvent](https://developer.mozilla.org/en-US/docs/Web/API/ClipboardEvent)
- [KeyboardEvent](https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent)
