---
cover_image: https://res.cloudinary.com/practicaldev/image/fetch/s--i0ViBxy6--/c_imagga_scale,f_auto,fl_progressive,h_420,q_auto,w_1000/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/5kybkw3w9lqa1khc0a1p.png
description: A ToDo App is a very beginner level app for any frontend developer. A
    basic ToDo app has...
id: 1031023
published: true
published_at: 2022-03-22 16:30:41.841000+00:00
slug: building-a-todo-app-in-react-51c8
tag_list:
- javascript
- react
- webdev
- tutorial
title: Building a ToDo App in React
---
A ToDo App is a very beginner level app for any frontend developer. A basic ToDo app has functionality of adding, deleting and updating the todos from the list. Being a developer, we easily tend to forget the tasks for the day or a span of time. It's always advisable to have such an app where we can add or delete or modify todos.

In this tutorial, let's design a ToDo App from scratch with basic crud (Create, Read, Update, Delete) functionality and added features like filter search, hide todos, and update status. 

## Getting Started

Creating a React App from cra-template using `create-react-app`, we will require no external libraries for the project, except `react-icons` that we will need for icons used in the application.

**ToDoApp.jsx**

```jsx
import React from 'react';

export default function ToDoApp() {
	return (
		<section className="ToDoApp">
			<h1>ToDo App</h1>
		</section>
	);
}
```

We will implement two components namely ToDoCard and ToDoForm for the app.

## Implementation

### Adding Basic Styles

**ToDoApp.css**

```css
.ToDoApp {
	width: 800px;
	max-width: 100%;
	margin: auto;
	padding: 0.5rem;
	color: var(--black);
}

.grey_text {
	color: var(--grey);
}
.red_text {
	color: var(--red);
}
.blue_text {
	color: var(--blue);
}
.green_text {
	color: var(--green);
}

.ToDoApp input,
.ToDoApp textarea,
.ToDoApp select {
	width: 100%;
	padding: 0.5rem 0.75rem;
}

.ToDoApp textarea {
	height: 10rem;
}

.ToDoApp button {
	padding: 0.5rem 1.5rem;
	background: var(--white);
	border: 1px solid var(--black);
}

.ToDoApp__Search {
	margin-top: 0.5rem;
	display: flex;
	gap: 1.5rem;
}

.ToDoApp__Search input {
	border: 1px solid var(--black);
}

/* @ToDoList Layout */

.ToDoList {
	height: 100%;
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	margin-top: 0.5rem;
}

.ToDoList__action {
	width: 100%;
}
```

### Card Component

Before we get started, let's install `react-icons` by executing 

```bash
npm i react-icons
```

Defining the json schema for each todo

```json
{
	"title": "string",
	"description": "string",
	"status": "integer(0,1,2)",
	"hide": "boolean",
	"id": "integer"
}
```

**ToDoCard.jsx**

```jsx
import React from 'react';
// Icons for Todo Card
import {
	FaCheckCircle,
	FaClock,
	FaExclamationCircle,
	FaEye,
	FaEyeSlash,
	FaPencilAlt,
	FaTimesCircle,
} from 'react-icons/fa';


export default function ToDoCard({
    id,
	title,
	description,
	status,
	hide,
	...otherProps
}){
    // Checking if the card is to be hidden
	if (hide) return null;
	
	return (
		<div className="ToDoCard" {...otherProps}>
			<div className="ToDoCard__left">
				<span>
					{status === 0 && <FaExclamationCircle title="Pending" className="ToDoCard__icon grey_text" />}
					{status === 1 && <FaClock title="Working" className="ToDoCard__icon blue_text" />}
					{status === 2 && <FaCheckCircle title="Done" className="ToDoCard__icon green_text" />}
				</span>
			</div>
			<div className="ToDoCard__center">
				<h2>{title}</h2>
			    <p>{description}</p>
			</div>
			<div className="ToDoCard__right">
				<FaTimesCircle
					className="ToDoCard__icon red_text"
				/>
				<span>
					<FaEye title="Show Description" className="ToDoCard__icon" />
				</span>

				<FaPencilAlt
					className="ToDoCard__icon"
				/>
			</div>
		</div>
	);
}
```
The ToDoCard component takes all properties of ToDo schema, where hide is used to return null on true and status shows three different symbols on three different integer values.

Furthermore we can toggle description using a state variable,

**ToDoCard.jsx**
```jsx
...
export default function ToDoCard({
...
}){
	const [showDescription, setShowDescription] = React.useState(false);
	...
	return (
		<div className="ToDoCard" {...otherProps}>
			...
			<div className="ToDoCard__center">
				<h2>{title}</h2>
				{showDescription && <p>{description}</p>}
			</div>
			<div className="ToDoCard__right">
				...
				<span
					onClick={() => {
						setShowDescription(!showDescription);
					}}
				>
					{showDescription && <FaEye title="Show Description" className="ToDoCard__icon" />}
					{!showDescription && <FaEyeSlash title="Hide Description" className="ToDoCard__icon" />}
				</span>
				...
			</div>
		</div>
	);
}
```
Using React.useState(), we solve the problem of visibility of description and its toggling.

Styling the card is less of a trouble,

**ToDoApp.css**
```css
...
/* @ToDo Card Layout */

.ToDoCard {
	border: 1px solid var(--black);
	width: 900px;
	max-width: 100%;
	padding: 0.5rem;
	font-size: 1rem;
	display: flex;
	flex-wrap: wrap;
	gap: 0.5rem;
}

.ToDoCard div {
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
}

.ToDoCard .ToDoCard__left {
	flex: 0 2.5rem;
}

.ToDoCard .ToDoCard__center {
	flex: 3;
	display: inline-block;
}

.ToDoCard .ToDoCard__right {
	flex: 0 2.5rem;
	gap: 0.5rem;
}

.ToDoCard h2 {
	font-size: larger;
}

.ToDoCard__icon {
	cursor: pointer;
}

@media screen and (max-width: 900px) {
	.ToDoCard {
		width: 100%;
		flex-direction: column;
	}
	.ToDoCard div {
		flex-direction: row;
		justify-content: flex-start;
	}
}
```

### Show/Hide Cards with Limit

In this section, we use a state variable *todos* to store the value of todos and a variable *maxDisplayTodos* for defining max no of visible todo cards.

**ToDoApp.jsx**
```jsx
import React from 'react';
import ToDoCard from './ToDoCard';
import './ToDoApp.css';
import { FaPlusCircle } from 'react-icons/fa';


export default function ToDoApp() {
	const [todos, setTodos] = React.useState([]);
	const [hideTodos, setHideTodos] = React.useState(true);
	
	const maxDisplayTodos = 5;
	
	React.useEffect(() => {
		setTodos([
			{
				title: 'Learn React',
				description: 'Learn React and its ecosystem',
				status: 0,
				hide: false,
				id: 1,
			},
			{
				title: 'Create a React Component',
				description:
					'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Veritatis esse aut similique reprehenderit fuga cupiditate porro. Nostrum, ipsam perferendis! Fuga nisi nostrum odit nulla quia, sint harum eligendi recusandae dolore!',
				status: 0,
				hide: false,
				id: 2,
			},
			{
				title: 'Learn Vue',
				description:
					'Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts. Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language ocean. A small river named Duden flows by their place and supplies it with the necessary.',
				status: 0,
				hide: false,
				id: 3,
			},
			{
				title: 'Learn Angular',
				description:
					'A wonderful serenity has taken possession of my entire soul, like these sweet mornings of spring which I enjoy with my whole heart. I am alone, and feel the charm of existence in this spot, which was created for the bliss of souls like mine. I am so happy, my',
				status: 0,
				hide: false,
				id: 4,
			},
			{
				title: 'Vue Typewriter',
				description:
					'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta.',
				status: 0,
				hide: false,
				id: 5,
			},
			{
				title: 'Learn jQuery',
				description:
					'Li Europan lingues es membres del sam familie. Lor separat existentie es un myth. Por scientie, musica, sport etc, litot Europa usa li sam vocabular. Li lingues differe solmen in li grammatica, li pronunciation e li plu commun vocabules. Omnicos directe al desirabilite de un nov lingua franca: On refusa',
				status: 0,
				hide: false,
				id: 14,
			},
			{
				title: 'Learn Javascript',
				description:
					'The European languages are members of the same family. Their separate existence is a myth. For science, music, sport, etc, Europe uses the same vocabulary. The languages only differ in their grammar, their pronunciation and their most common words. Everyone realizes why a new common language would be desirable: one',
				status: 0,
				hide: false,
				id: 15,
			},
		]);
	}, []);
	
	function handleHideTodos() {
		const newHideTodos = !hideTodos;
		setHideTodos(newHideTodos);
		if (newHideTodos) {
			const newTodos = todos.map((todo, index) => {
				if (index >= maxDisplayTodos) todo.hide = false;
				return todo;
			});
			setTodos(newTodos);
		} else {
			const newTodos = todos.map((todo, index) => {
				if (index >= maxDisplayTodos) todo.hide = true;
				return todo;
			});
			setTodos(newTodos);
		}
	}
	
	
	return (
		<section className="ToDoApp">
			<h1>ToDo App</h1>
			<div className="ToDoList">
				{(todos || []).map((todo, index) => (
					<ToDoCard
						key={index}
						{...todo}
					/>
				))}
				{(!todos || todos.length === 0) && (
					<div className="ToDoList__empty">
						<p>No todos found</p>
					</div>
				)}
				{todos.length > maxDisplayTodos && (
					<button className="ToDoList__action" type="button" onClick={() => handleHideTodos()}>
						{hideTodos ? 'HIDE' : 'SHOW'}
					</button>
				)}
			</div>
		</section>
	);
	
}
```

There is another state variable *hideTodos* used to determine when to hide the todos and when not to. Also there is a function *handleHideTodos()* that handles the state variable *hideTodos* and based on the current status of hideTodos we either hide or show off the *maxDisplayTodos* limit. We also have a no todos found for no todos and a togglable show/hide button based on *hideTodos*.

### Form Component

Before we start on with the add, edit and delete of todos, let's introduce our form component. 

**ToDoForm.jsx**

```jsx
import React from 'react';
import { FaTimes } from 'react-icons/fa';

function ToDoForm({
	title: titleProps,
	description: descriptionProps,
	status: statusProps,
	id,
}) {
	const [title, setTitle] = React.useState(titleProps);
	const [description, setDescription] = React.useState(descriptionProps);
	const [status, setStatus] = React.useState(statusProps);
	
	function handleTitleChange(e) {
		setTitle(e.target.value);
	}

	function handleDescriptionChange(e) {
		setDescription(e.target.value);
	}

	function handleStatusChange(e) {
		setStatus(parseInt(e.target.value));
	}
	
	return (
		<form className="ToDoForm">
			<FaTimes className="close-btn"/>
			<h2>ToDo Form</h2>
			<div className="ToDoForm__field">
				<label htmlFor="title">Title</label>
				<input type="text" id="title" value={title} onChange={(e) => handleTitleChange(e)} />
			</div>
			<div className="ToDoForm__field">
				<label htmlFor="description">Description</label>
				<textarea
					type="text"
					id="description"
					value={description}
					onChange={(e) => handleDescriptionChange(e)}
				/>
			</div>
			<div className="ToDoForm__field">
				<label htmlFor="status">Status</label>
				<select id="status" value={status} onChange={(e) => handleStatusChange(e)}>
					<option value="0">Pending</option>
					<option value="1">Working</option>
					<option value="2">Done</option>
				</select>
			</div>
			<div className="ToDoForm__action">
				<button type="submit">{id === -1 ? 'Add' : 'Update'}</button>
			</div>
		</form>
	);
}

ToDoForm.defaultProps = {
	title: '',
	description: '',
	status: 0,
	id: -1,
};

export default ToDoForm;
```

Handling form elements poses a trouble in React if being handled with state variables, we need to handle inputChange with event handler. So there are three state variables (*title*, *description* and *status*) and three inputChange handlers (*handleTitleChange*, *handleDescriptionChange*, *handleStatusChange*). 

Styling ToDoForm Component

**ToDoApp.css**

```css
...
/* @ToDo Form Layout */
.ToDoForm {
	padding: 0.5rem;
	border: 1px solid var(--black);
	margin-top: 1rem;
	display: flex;
	flex-direction: column;
	gap: 0.5rem;
	justify-content: space-around;
	position: relative;
}
.ToDoForm .close-btn {
	position: absolute;
	right: 0.5rem;
	top: 0.5rem;
}
.ToDoForm__field,
.ToDoForm__action {
	display: flex;
	align-items: center;
	flex-direction: row;
	gap: 0.5rem;
}
.ToDoForm__field label {
	flex: 0 0 6rem;
	font-size: 1rem;
}
.ToDoForm__action button {
	margin-left: auto;
}
```

### Adding Form Component & Close Form

**ToDoApp.jsx**

```jsx
...
export default function ToDoApp(){
	...
	const [showForm, setShowForm] = React.useState(false);
	
	...
	
	return (
		<section className="ToDoApp">
			...
			{showForm && (
				<ToDoForm
					closeForm={() => {
						setShowForm(false);
					}}
				/>
			)}
		</section>
	);
}
```

Added a *showForm* state variable, pass it to the form component.

**ToDoForm.jsx**

```jsx
...
function ToDoForm({
	title: titleProps,
	description: descriptionProps,
	status: statusProps,
	id,
	closeForm,
)} {
	...
	function handleCloseForm() {
		setTitle('');
		setDescription('');
		setStatus(0);
		closeForm();
	}

	return (
		<form className="ToDoForm">
			<FaTimes className="close-btn" onClick={() => handleCloseForm()} />
			...
		</form>
	);
}
...
```

Adding a handler for closeform with setting all state variables to initial state.

### Searching Todo Items

**ToDoApp.jsx**

```jsx
...
export default function ToDoApp() {
	...
	const [searchText, setSearchText] = React.useState('');

	...

	function handleSearchChange(evt) {
		setSearchText(evt.target.value);

		const newTodos = todos.map((todo) => {
			todo.hide = !(
				todo.title.toLowerCase().includes(evt.target.value.toLowerCase()) ||
				todo.description.toLowerCase().includes(evt.target.value.toLowerCase())
			);
			return todo;
		});
		setTodos(newTodos);
	}

	return (
		<section className="ToDoApp">
			<h1>ToDo App</h1>
			<div className="ToDoApp__Search">
				<input
					type="text"
					value={searchText}
					onChange={(evt) => handleSearchChange(evt)}
					placeholder="Search"
				/>
				<button className="ToDoApp__create_btn">
					<FaPlusCircle />
				</button>
			</div>
			...
		</section>

	);
}
```

Used a state variable *searchText* for storing search input value, also handled the search change with hiding the list that didn't match the search. In case of long list, might have queried it from a database with a loader.

### Add Todo Items

**ToDoApp.jsx**

```jsx
...
export default function ToDoApp() {
	...

	function handleAddTodo(todo) {
		const newTodo = {
			title: todo.title,
			description: todo.description,
			status: 0,
			hide: false,
			id: Date.now() % 1000000,
		};
		setTodos([...todos, newTodo]);
		setShowForm(false);		
	}
	...
	return (
		<section className="ToDoApp">
			<h1>ToDo App</h1>
			<div className="ToDoApp__Search">
				...
				<button className="ToDoApp__create_btn" onClick={() => setShowForm(true)}>
					<FaPlusCircle />
				</button>
			</div>

			{showForm && (
				<ToDoForm
					handleAddTodo={handleAddTodo}
					closeForm={() => {
						setShowForm(false);
					}}
				/>
			)}
			...
		</section>
	);
}

```

Defining a *handleAddToDo* handler function, to add a new ToDo object to the ToDos and maintaining closing form on submit. Opening form on click of create Todo button.

**ToDoForm.jsx**

```jsx
...
function ToDoForm({
	title: titleProps,
	description: descriptionProps,
	status: statusProps,
	id,
	closeForm,
	handleAddTodo,
}) {
	...

	function handleFormSubmit(e) {
		e.preventDefault();
		if (title === '' || description === '') {
			alert('Please fill in all fields');
			return;
		}
		handleAddTodo({ title, description, status });
		setTitle('');
		setDescription('');
		setStatus(0);
	}

	return (
		<form className="ToDoForm" onSubmit={(e) => handleFormSubmit(e)}>
			...
		</form>
	);
}
...
```

Defining *handleFormSubmit* function to set to initial values and trigger addtodo handler.

### Edit Todo Item

Editing Todo Item is little bit tricky, because we need remember the id of the element to be edit with its value passed onto the todo form. Let's see how that happens.

**ToDoApp.jsx**

```jsx
...
export default function ToDoApp() {
	const [currentTodo, setCurrentTodo] = React.useState({});
	...
	function handleEditTodo(id) {
		setShowForm(true);
		const todo = todos.find((todo) => todo.id === id);
		setCurrentTodo(todo);
	}

	function handleAddTodo(todo) {
		if (todo.id === undefined) {
			const newTodo = {
				title: todo.title,
				description: todo.description,
				status: 0,
				hide: false,
				id: Date.now() % 1000000,
			};
			setTodos([...todos, newTodo]);
		} else {
			const newTodos = todos.map((todo_) => {
				if (todo.id === todo_.id) {
					todo_.title = todo.title;
					todo_.description = todo.description;
					todo_.status = todo.status;
				}
				return todo_;
			});
			setTodos(newTodos);
		}
		setCurrentTodo({});
		setShowForm(false);
	}

	return (
		<section className="ToDoApp">
			...

			{showForm && (
				<ToDoForm
					handleAddTodo={handleAddTodo}
					{...currentTodo}
					closeForm={() => {
						setCurrentTodo({});
						setShowForm(false);
					}}
				/>
			)}


			<div className="ToDoList">
				{(todos || []).map((todo, index) => (
					<ToDoCard
						key={index}
						{...todo}
						handleEditTodo={handleEditTodo}
					/>
				))}
				...
			</div>
		</section>
	);
}
```

Adding a state variable *currentTodo* to set the current Todo object for edit and passing as prop to the ToDo Form and also modifying *handleAddTodo* function to update already existing Todo object. Add *handleEditTodo* function to set *currentTodo* for current element.

**ToDoForm.jsx**

```jsx
...
function ToDoForm({
	title: titleProps,
	description: descriptionProps,
	status: statusProps,
	id,
	closeForm,
	handleAddTodo,
}) {
	...

	function handleFormSubmit(e) {
		e.preventDefault();
		if (title === '' || description === '') {
			alert('Please fill in all fields');
			return;
		}
		if (id >= 0) handleAddTodo({ title, description, status, id: id });
		else handleAddTodo({ title, description, status });
		setTitle('');
		setDescription('');
		setStatus(0);
	}
	...
}
...
```

Modifying *handleFormSubmit* function to handle both create and update cases.

**ToDoCard.jsx**

```jsx
...
export default function ToDoCard({
	id,
	title,
	description,
	status,
	hide,
	handleEditTodo,
	...otherProps
}){
	...
	return (
		<div className="ToDoCard" {...otherProps}>
			...
			<div className="ToDoCard__right">
				...
				<FaPencilAlt
					className="ToDoCard__icon"
					onClick={() => {
						handleEditTodo(id);
					}}
				/>
			</div>
		</div>
	);
}

```

Triggering *handleEditTodo* function for current ToDo element.

### Delete ToDo

**ToDoApp.jsx**

```jsx
...

export default function ToDoApp() {
	...

	function handleDeleteTodo(id) {
		const newTodos = todos.filter((todo) => todo.id !== id);
		setTodos(newTodos);
	}

	return (
		<section className="ToDoApp">
			...

			<div className="ToDoList">
				{(todos || []).map((todo, index) => (
					<ToDoCard
						key={index}
						{...todo}
						handleEditTodo={handleEditTodo}
						handleDeleteTodo={handleDeleteTodo}
					/>
				))}
				...
			</div>
		</section>
	);
}
```

Creating a *handleDeleteTodo* function for an id, updating the todos without the given id todo object and pass on to ToDoCard. 

**ToDoCard.jsx**

```jsx
...
export default function ToDoCard({
	id,
	title,
	description,
	status,
	hide,
	handleEditTodo,
	handleDeleteTodo,
	...otherProps
}){
	...
	return (
		<div className="ToDoCard" {...otherProps}>
			...
			<div className="ToDoCard__right">
				<FaTimesCircle
					className="ToDoCard__icon red_text"
					onClick={() => {
						handleDeleteTodo(id);
					}}
				/>
				...
			</div>
		</div>
	);
}
...

```

ToDoCard element on click of delete button trigger *handleDeleteTodo* for current element id.

### Change Status

**ToDoApp.jsx**

```jsx
...
export default function ToDoApp() {
	...

	function handleChangeStatus(id) {
		const newTodos = todos.map((todo) => {
			if (todo.id === id) {
				todo.status = todo.status === 2 ? 0 : todo.status + 1;
			}
			return todo;
		});
		setTodos(newTodos);
	}

	
	return (
		<section className="ToDoApp">
			...

			<div className="ToDoList">
				{(todos || []).map((todo, index) => (
					<ToDoCard
						key={index}
						{...todo}
						handleChangeStatus={handleChangeStatus}
						handleEditTodo={handleEditTodo}
						handleDeleteTodo={handleDeleteTodo}
					/>
				))}
				...
			</div>
		</section>
	);	
}
```

Added a handler for changestatus for id and is passed to ToDoCard for invokation. The handler updates the last status from 0 to 2 and back to 0 in a circular fashion.

**ToDoCard.jsx**

```jsx
...
export default function ToDoCard({
	id,
	title,
	description,
	status,
	hide,
	handleEditTodo,
	handleDeleteTodo,
	handleChangeStatus,
	...otherProps
}) {
	...

	return (
		<div className="ToDoCard" {...otherProps}>
			<div className="ToDoCard__left">
				<span
					onClick={() => {
						handleChangeStatus(id);
					}}
				>
					{status === 0 && <FaExclamationCircle title="Pending" className="ToDoCard__icon grey_text" />}
					{status === 1 && <FaClock title="Working" className="ToDoCard__icon blue_text" />}
					{status === 2 && <FaCheckCircle title="Done" className="ToDoCard__icon green_text" />}
				</span>
			</div>
			...
		</div>
	);
}

```

Passed function for status change is onclick triggered for status icon that is changed with varied status value.

## Final Code

**ToDoApp.css**
<https://github.com/shivishbrahma/nuclear-reactor/blob/main/src/ToDoApp/ToDoApp.css>

**ToDoApp.jsx**
<https://github.com/shivishbrahma/nuclear-reactor/blob/main/src/ToDoApp/ToDoApp.jsx>

**ToDoCard.jsx**
<https://github.com/shivishbrahma/nuclear-reactor/blob/main/src/ToDoApp/ToDoCard.jsx>

**ToDoForm.jsx**
<https://github.com/shivishbrahma/nuclear-reactor/blob/main/src/ToDoApp/ToDoForm.jsx>

## Preview

![Preview of TodoApp](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/kwuku2famd9mqed5fin6.png)
