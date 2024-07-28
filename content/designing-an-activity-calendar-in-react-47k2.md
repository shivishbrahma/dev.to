---
cover_image: https://media.dev.to/cdn-cgi/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fvptsqyr0ivfbzur7375s.png
created_at: 2022-02-27 07:48:23+00:00
description: Activity Calendar has become popular after open-source platforms like
    Github, Kaggle starting used to...
edited_at: 2024-07-28 05:01:23+00:00
id: 1002962
published: true
published_at: 2022-02-27 07:48:23+00:00
series: 17308
slug: designing-an-activity-calendar-in-react-47k2
tags:
- javascript
- react
- component
- github
title: Designing an Activity Calendar in React
---
Activity Calendar has become popular after open-source platforms like Github, Kaggle starting used to show contributions data in this format. As a developer, people often tries to analyse what are the days I am productive the most. The measure might be a quantitative and not qualitative, but it gives a clear picture overall. We gonna build an Activity Calendar Component today in React from Scratch.

![A Pacman Inspired Activity Calendar ASCII Art](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/q771tsqwnk0k1wody5dm.png)

Activity Calendar or Graph is a heatmap graph distribution over months and days of week.

## Getting Started

Starting from the basic cra-template of creact-react app

**ActivityCalendar.jsx**

```jsx
import React from 'react';

function ActivityCalendar({ children, style, ...otherProps }) {
	return (
		<article className="ActivityCalendar" style={style} {...otherProps}>
			<svg></svg>
			{children}
		</article>
	);
}

export default ActivityCalendar;
```

This functional component has **children** and **style** props where children helps to populate any child component and style to populate with inline CSS style.

## Implementation

### Formatting Data

We need to have some utilities function to format data or generate an empty data. Few libraries that we need to install here are a colour utility library `tinycolor2` and a date manipulation library `date-fns`.

```sh
npm install tinycolor2 date-fns
```

#### NormalizeCalendarDays

**util.js**

```js
import eachDayOfInterval from 'date-fns/eachDayOfInterval';
import formatISO from 'date-fns/formatISO';
import parseISO from 'date-fns/parseISO';

function normalizeCalendarDays(days) {
	const daysMap = days.reduce((map, day) => {
		map.set(day.date, day);
		return map;
	}, new Map());

	return eachDayOfInterval({
		start: parseISO(days[0].date),
		end: parseISO(days[days.length - 1].date),
	}).map((day) => {
		const date = formatISO(day, { representation: 'date' });

		if (daysMap.has(date)) {
			return daysMap.get(date);
		}

		return {
			date,
			count: 0,
			level: 0,
		};
	});
}

```

The function *normalizeCalendarDays* takes in list of days and creates a daysMap for each date. The daysMap is used to get all the days from starting date to ending date, and if a date is missing in the array days, a default count and level of 0 is added to the resulting array against that date.

#### Group by Weeks

**utils.js**

```js
...
import parseISO from 'date-fns/parseISO';
import differenceInCalendarDays from 'date-fns/differenceInCalendarDays';
import getDay from 'date-fns/getDay';
import subWeeks from 'date-fns/subWeeks';
import nextDay from 'date-fns/nextDay';

...
export function groupByWeeks(days, weekStart) {
	if (days.length === 0) return [];

	// The calendar expects a continuous sequence of days, so fill gaps with empty activity.
	const normalizedDays = normalizeCalendarDays(days);

	// Determine the first date of the calendar. If the first contribution date is not
	// specified week day the desired day one week earlier will be selected.
	const firstDate = parseISO(normalizedDays[0].date);
	const firstCalendarDate = getDay(firstDate) === weekStart ? firstDate : subWeeks(nextDay(firstDate, weekStart), 1);

	// In order to correctly group contributions by week it is necessary to left pad the list,
	// because the first date might not be desired week day.
	const paddedDays = [
		...Array(differenceInCalendarDays(firstDate, firstCalendarDate)).fill(undefined),
		...normalizedDays,
	];

	return Array(Math.ceil(paddedDays.length / 7))
		.fill(undefined)
		.map((_, calendarWeek) => paddedDays.slice(calendarWeek * 7, calendarWeek * 7 + 7));
}
```

The function *groupByWeeks* takes in list of days (**days**) and **weekStart** as input parameters where it groups the given list of days into weeks starting with weekStart.

#### Get Labels for Months

**utils.js**

```js
...
import nextDay from 'date-fns/nextDay';
import getMonth from 'date-fns/getMonth';
...

export const MIN_DISTANCE_MONTH_LABELS = 2;
export const DEFAULT_MONTH_LABELS = [
	'Jan',
	'Feb',
	'Mar',
	'Apr',
	'May',
	'Jun',
	'Jul',
	'Aug',
	'Sep',
	'Oct',
	'Nov',
	'Dec',
];

...
export function getMonthLabels(weeks, monthNames = DEFAULT_MONTH_LABELS) {
	return weeks
		.reduce((labels, week, index) => {
			const firstWeekDay = week.find((day) => day !== undefined);

			if (!firstWeekDay) {
				throw new Error(`Unexpected error: Week is empty: [${week}]`);
			}

			const month = monthNames[getMonth(parseISO(firstWeekDay.date))];
			const prev = labels[labels.length - 1];

			if (index === 0 || prev.text !== month) {
				return [
					...labels,
					{
						x: index,
						y: 0,
						text: month,
					},
				];
			}

			return labels;
		}, [])
		.filter((label, index, labels) => {
			if (index === 0) {
				return labels[1] && labels[1].x - label.x > MIN_DISTANCE_MONTH_LABELS;
			}

			return true;
		});
}
```

The function **getMonthLabels** takes in list of weeks and monthNames as input parameters. For each week, find the first day and get the monthName for the first day. If the last month in the label is not same or it's first value then x and y is set to 0 else return labels. Filter out the labels for each starting index with greater than minimum distance between the labels or other indexes.

#### Creating a Calendar Theme

**utils.js**

```jsx
...
import getMonth from 'date-fns/getMonth';
import color from 'tinycolor2';

const DEFAULT_THEME = createCalendarTheme('#042a33');
...
export function createCalendarTheme(baseColor, emptyColor = color('white').darken(8).toHslString()) {
	const base = color(baseColor);

	if (!base.isValid()) {
		return DEFAULT_THEME;
	}

	return {
		level4: base.setAlpha(0.44).toHslString(),
		level3: base.setAlpha(0.6).toHslString(),
		level2: base.setAlpha(0.76).toHslString(),
		level1: base.setAlpha(0.92).toHslString(),
		level0: emptyColor,
	};
}
```

The function **createCalendarTheme** takes baseColor and emptyColor as input parameters and returns a theme with 5 different colors for each level.

#### Helper Functions

**utils.js**

```js
...
export const NAMESPACE = 'ActivityCalendar';

export const DEFAULT_WEEKDAY_LABELS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

export const DEFAULT_LABELS = {
	months: DEFAULT_MONTH_LABELS,
	weekdays: DEFAULT_WEEKDAY_LABELS,
	totalCount: '{{count}} contributions in {{year}}',
	legend: {
		less: 'Less',
		more: 'More',
	},
};
...

export function getTheme(theme, color) {
	if (theme) {
		return Object.assign({}, DEFAULT_THEME, theme);
	}

	if (color) {
		return createCalendarTheme(color);
	}

	return DEFAULT_THEME;
}

export function getClassName(name, styles) {
	if (styles) {
		return `${NAMESPACE}__${name} ${styles}`;
	}

	return `${NAMESPACE}__${name}`;
}

export function generateEmptyData() {
	const year = new Date().getFullYear();
	const days = eachDayOfInterval({
		start: new Date(year, 0, 1),
		end: new Date(year, 11, 31),
	});

	return days.map((date) => ({
		date: formatISO(date, { representation: 'date' }),
		count: 0,
		level: 0,
	}));
}

```

### Calculating Size

**ActivityCalendar.jsx**

```jsx
import React from 'react';

import { groupByWeeks } from './utils';

function ActivityCalendar({
	blockMargin,
	children,
	color,
	data,
	fontSize,
	hideMonthLabels,
	labels: labelsProp,
	style,
	theme: themeProp,
	weekStart,
	...otherProps
}) {
	if (data.length === 0) return null;

	const weeks = groupByWeeks(data, weekStart);
	const textHeight = hideMonthLabels ? 0 : fontSize + 2 * blockMargin;
    
    function getDimensions() {
		return {
			width: weeks.length * (blockSize + blockMargin) - blockMargin,
			height: textHeight + (blockSize + blockMargin) * 7 - blockMargin,
		};
	}
...
}

ActivityCalendar.defaultProps = {
	blockMargin: 4,
	blockSize: 12,
	color: undefined,
	fontSize: 14,
	hideMonthLabels: false,
	style: {},
	weekStart: 0,
};
...
```

Using **blockSize**, **blockMargin**, length of **weeks** array and **textHeight**, calculate width and height of the Activity Calendar.

### Adding Styles Module

**styles.module.css**

```css
.calendar {
	display: block;
	max-width: 100%;
	height: auto;
	overflow: visible;
}

.calendar text {
	fill: currentColor;
}

.block {
	stroke: rgba(0, 0, 0, 0.1);
	stroke-width: 1px;
	shape-rendering: geometricPrecision;
}

.footer {
	display: flex;
}

.legendColors {
	margin-left: auto;
	display: flex;
	align-items: center;
	gap: 0.2em;
}

@keyframes loadingAnimation {
	0% {
		fill: var(--ActivityCalendar-loading);
	}
	50% {
		fill: var(--ActivityCalendar-loading-active);
	}
	100% {
		fill: var(--ActivityCalendar-loading);
	}
}
```

Using CSS module, ActivityCalendar uses loadingAnimation and other necessary styles.

### Rendering Blocks

**ActivityCalendar.jsx**

```jsx
...
import { getClassName, getTheme, groupByWeeks, NAMESPACE } from './utils';

import styles from './styles.module.css';
import tinycolor from 'tinycolor2';

function ActivityCalendar({
	blockMargin,
	blockRadius,
	blockSize,
	children,
	color,
	data,
	dateFormat,
	fontSize,
	hideMonthLabels,
	loading,
	labels: labelsProp,
	style,
	theme: themeProp,
	weekStart,
	...otherProps
}) {
	if (loading) data = generateEmptyData();
	...
    const theme = getTheme(themeProp, color);
    ...

    function renderBlocks() {
        return weeks
            .map((week, weekIndex) =>
                week.map((day, dayIndex) => {
                    if (!day) {
                        return null;
                    }

                    const style = loading
                        ? {
                                animation: `${styles.loadingAnimation} 1.5s ease-in-out infinite`,
                                animationDelay: `${weekIndex * 20 + dayIndex * 20}ms`,
                          }
                        : undefined;

                    return (
                        <rect
                            // {...getEventHandlers(day)}
                            x={0}
                            y={textHeight + (blockSize + blockMargin) * dayIndex}
                            width={blockSize}
                            height={blockSize}
                            fill={theme[`level${day.level}`]}
                            rx={blockRadius}
                            ry={blockRadius}
                            className={styles.block}
                            data-date={day.date}
                            key={day.date}
                            style={style}
                        />
                    );
                })
            )
            .map((week, x) => (
                <g key={x} transform={`translate(${(blockSize + blockMargin) * x}, 0)`}>
                    {week}
                </g>
            ));
    }
    const { width, height } = getDimensions();
	const additionalStyles = {
		maxWidth: width,
		// Required for correct colors in CSS loading animation
		[`--${NAMESPACE}-loading`]: theme.level0,
		[`--${NAMESPACE}-loading-active`]: tinycolor(theme.level0).darken(8).toString(),
	};

	return (
		<article className="ActivityCalendar" style={{ ...style, ...additionalStyles }} {...otherProps}>
			<svg
				className={getClassName('calendar', styles.calendar)}
				width={width}
				height={height}
				viewBox={`0 0 ${width} ${height}`}
			>
				{renderBlocks()}
			</svg>
			{children}
		</article>
	);
}
...
```

The function *renderBlocks* renders coloured blocks for each day chunked in weeks and coloured according to the theme.

### Rendering Labels

**ActivityCalendar.jsx**

```jsx
...
import getDay from 'date-fns/getDay';

import { DEFAULT_LABELS, DEFAULT_WEEKDAY_LABELS, generateEmptyData, getClassName, getMonthLabels, getTheme, groupByWeeks, MIN_DISTANCE_MONTH_LABELS, NAMESPACE } from './utils';
...

function ActivityCalendar({
	blockMargin,
	blockRadius,
	blockSize,
	children,
	color,
	data,
	dateFormat,
	fontSize,
	hideMonthLabels,
	loading,
	labels: labelsProp,
	style,
    showWeekdayLabels,
	theme: themeProp,
	weekStart,
	...otherProps
}) {
	if (loading) data = generateEmptyData();
    
	if (data.length === 0) return null;

	const weeks = groupByWeeks(data, weekStart);
	const textHeight = hideMonthLabels ? 0 : fontSize + 2 * blockMargin;
	const theme = getTheme(themeProp, color);
	const labels = Object.assign({}, DEFAULT_LABELS, labelsProp);
    ...
    
	function renderLabels() {
		const style = {
			fontSize,
		};

		if (!showWeekdayLabels && hideMonthLabels) {
			return null;
		}

		return (
			<>
				{showWeekdayLabels && (
					<g className={getClassName('legend-weekday')} style={style}>
						{weeks[1].map((day, y) => {
							if (!day || y % 2 === 0) {
								return null;
							}

							const dayIndex = getDay(parseISO(day.date));

							return (
								<text
									x={-2 * blockMargin}
									y={textHeight + (fontSize / 2 + blockMargin) + (blockSize + blockMargin) * y}
									textAnchor="end"
									key={day.date}
								>
									{labels.weekdays ? labels.weekdays[dayIndex] : DEFAULT_WEEKDAY_LABELS[dayIndex]}
								</text>
							);
						})}
					</g>
				)}
				{!hideMonthLabels && (
					<g className={getClassName('legend-month')} style={style}>
						{getMonthLabels(weeks, labels.months).map(({ text, x }, index, labels) => {
							// Skip the first month label if there's not enough space to the next one
							if (index === 0 && labels[1] && labels[1].x - x <= MIN_DISTANCE_MONTH_LABELS) {
								return null;
							}

							return (
								<text x={(blockSize + blockMargin) * x} alignmentBaseline="hanging" key={x}>
									{text}
								</text>
							);
						})}
					</g>
				)}
			</>
		);
	}
...

	return (
		<article className="ActivityCalendar" style={{ ...style, ...additionalStyles }} {...otherProps}>
			<svg
				className={getClassName('calendar', styles.calendar)}
				width={width}
				height={height}
				viewBox={`0 0 ${width} ${height}`}
			>
				{!loading && renderLabels()}
				{renderBlocks()}
			</svg>
			{children}
		</article>
	);
    
}
...

```

The function *renderLabels* renders labels for weeks and days based on **hideMonthLabels**(props) and **showWeekdayLabels**(props).

### Render Footer

**ActivityCalendar.jsx**

```jsx
...
import {
	DEFAULT_LABELS,
	DEFAULT_WEEKDAY_LABELS,
	generateEmptyData,
	getClassName,
	getMonthLabels,
	getTheme,
	groupByWeeks,
	MIN_DISTANCE_MONTH_LABELS,
	NAMESPACE,
} from './utils';

...

function ActivityCalendar({
	blockMargin,
	blockRadius,
	blockSize,
	children,
	color,
	data,
	dateFormat,
	fontSize,
	hideColorLegend,
	hideMonthLabels,
	hideTotalCount,
	loading,
	labels: labelsProp,
	style,
	showWeekdayLabels,
	theme: themeProp,
	weekStart,
	...otherProps
}) {
    ...
	const labels = Object.assign({}, DEFAULT_LABELS, labelsProp);
	const totalCount = data.reduce((sum, day) => sum + day.count, 0);
	const year = getYear(parseISO(data[0].date));
	....

    function renderFooter() {
		if (hideTotalCount && hideColorLegend) {
			return null;
		}

		return (
			<footer className={getClassName('footer', styles.footer)} style={{ marginTop: 2 * blockMargin, fontSize }}>
				{/* Placeholder */}
				{loading && <div>&nbsp;</div>}

				{!loading && !hideTotalCount && (
					<div className={getClassName('count')}>
						{labels.totalCount
							? labels.totalCount
									.replace('{{count}}', String(totalCount))
									.replace('{{year}}', String(year))
							: `${totalCount} contributions in ${year}`}
					</div>
				)}

				{!loading && !hideColorLegend && (
					<div className={getClassName('legend-colors', styles.legendColors)}>
						<span style={{ marginRight: '0.4em' }}>{labels.legend.less ?? 'Less'}</span>
						{Array(5)
							.fill(undefined)
							.map((_, index) => (
								<svg width={blockSize} height={blockSize} key={index}>
									<rect
										width={blockSize}
										height={blockSize}
										fill={theme[`level${index}`]}
										rx={blockRadius}
										ry={blockRadius}
									/>
								</svg>
							))}
						<span style={{ marginLeft: '0.4em' }}>{labels.legend.more ?? 'More'}</span>
					</div>
				)}
			</footer>
		);
	}

    ...

	return (
		<article className="ActivityCalendar" style={{ ...style, ...additionalStyles }} {...otherProps}>
			<svg
				className={getClassName('calendar', styles.calendar)}
				width={width}
				height={height}
				viewBox={`0 0 ${width} ${height}`}
			>
				{!loading && renderLabels()}
				{renderBlocks()}
			</svg>
			{renderFooter()}
			{children}
		</article>
	);
}

...
```

The function *renderFooter* renders the footer with total no of contributions and **showsLegend** for colours used in the heatmap graph.

## Final Code

**ActivityCalendar.jsx**

<https://github.com/shivishbrahma/nuclear-reactor/blob/main/src/ActivityCalendar/ActivityCalendar.jsx>

**utils.js**

<https://github.com/shivishbrahma/nuclear-reactor/blob/main/src/ActivityCalendar/utils.js>

**styles.module.css**

<https://github.com/shivishbrahma/nuclear-reactor/blob/main/src/ActivityCalendar/styles.module.css>

## Use within App component

```jsx
import ActivityCalendar from './ActivityCalendar';
import './App.css';

const DEFAULT_THEME = {
		level4: '#216e39',
		level3: '#30a14e',
		level2: '#40c463',
		level1: '#9be9a8',
		level0: '#ebedf0',
	},
	calendarData = [
		{
			count: 0,
			date: '2022-01-01',
			level: 0,
		},
		{
			count: 0,
			date: '2022-01-02',
			level: 0,
		}
		...
	];
function App() {
	return (
		<div className="App">
			<ActivityCalendar data={calendarData} theme={DEFAULT_THEME}/>
		</div>
	);
}

export default App;
```

## Preview

![Preview of Activity Calendar Component](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/anyjk26q63at2ej1spsi.png)

## Reference

- [React Activity Calendar](https://www.npmjs.com/package/react-activity-calendar)
