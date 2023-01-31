---
cover_image: https://res.cloudinary.com/practicaldev/image/fetch/s--sZ0I69e6--/c_imagga_scale,f_auto,fl_progressive,h_420,q_auto,w_1000/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/vptsqyr0ivfbzur7375s.png
description: Activity Calendar has become popular after open-source platforms like
  Github, Kaggle starting used to...
id: 1002962
published: true
published_at: '2022-02-27T07:48:23.025Z'
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
		},
		{
			count: 0,
			date: '2022-01-03',
			level: 0,
		},
		{
			count: 0,
			date: '2022-01-04',
			level: 0,
		},
		{
			count: 0,
			date: '2022-01-05',
			level: 0,
		},
		{
			count: 1,
			date: '2022-01-06',
			level: 1,
		},
		{
			count: 1,
			date: '2022-01-07',
			level: 1,
		},
		{
			count: 10,
			date: '2022-01-08',
			level: 4,
		},
		{
			count: 9,
			date: '2022-01-09',
			level: 4,
		},
		{
			count: 2,
			date: '2022-01-10',
			level: 1,
		},
		{
			count: 5,
			date: '2022-01-11',
			level: 2,
		},
		{
			count: 1,
			date: '2022-01-12',
			level: 1,
		},
		{
			count: 1,
			date: '2022-01-13',
			level: 1,
		},
		{
			count: 0,
			date: '2022-01-14',
			level: 0,
		},
		{
			count: 6,
			date: '2022-01-15',
			level: 3,
		},
		{
			count: 4,
			date: '2022-01-16',
			level: 2,
		},
		{
			count: 0,
			date: '2022-01-17',
			level: 0,
		},
		{
			count: 7,
			date: '2022-01-18',
			level: 3,
		},
		{
			count: 1,
			date: '2022-01-19',
			level: 1,
		},
		{
			count: 6,
			date: '2022-01-20',
			level: 3,
		},
		{
			count: 6,
			date: '2022-01-21',
			level: 3,
		},
		{
			count: 0,
			date: '2022-01-22',
			level: 0,
		},
		{
			count: 2,
			date: '2022-01-23',
			level: 1,
		},
		{
			count: 0,
			date: '2022-01-24',
			level: 0,
		},
		{
			count: 0,
			date: '2022-01-25',
			level: 0,
		},
		{
			count: 4,
			date: '2022-01-26',
			level: 2,
		},
		{
			count: 0,
			date: '2022-01-27',
			level: 0,
		},
		{
			count: 0,
			date: '2022-01-28',
			level: 0,
		},
		{
			count: 5,
			date: '2022-01-29',
			level: 2,
		},
		{
			count: 1,
			date: '2022-01-30',
			level: 1,
		},
		{
			count: 5,
			date: '2022-01-31',
			level: 2,
		},
		{
			count: 0,
			date: '2022-02-01',
			level: 0,
		},
		{
			count: 4,
			date: '2022-02-02',
			level: 2,
		},
		{
			count: 1,
			date: '2022-02-03',
			level: 1,
		},
		{
			count: 4,
			date: '2022-02-04',
			level: 2,
		},
		{
			count: 4,
			date: '2022-02-05',
			level: 2,
		},
		{
			count: 3,
			date: '2022-02-06',
			level: 2,
		},
		{
			count: 1,
			date: '2022-02-07',
			level: 1,
		},
		{
			count: 3,
			date: '2022-02-08',
			level: 2,
		},
		{
			count: 3,
			date: '2022-02-09',
			level: 2,
		},
		{
			count: 0,
			date: '2022-02-10',
			level: 0,
		},
		{
			count: 3,
			date: '2022-02-11',
			level: 2,
		},
		{
			count: 0,
			date: '2022-02-12',
			level: 0,
		},
		{
			count: 5,
			date: '2022-02-13',
			level: 2,
		},
		{
			count: 0,
			date: '2022-02-14',
			level: 0,
		},
		{
			count: 1,
			date: '2022-02-15',
			level: 1,
		},
		{
			count: 6,
			date: '2022-02-16',
			level: 3,
		},
		{
			count: 2,
			date: '2022-02-17',
			level: 1,
		},
		{
			count: 4,
			date: '2022-02-18',
			level: 2,
		},
		{
			count: 5,
			date: '2022-02-19',
			level: 2,
		},
		{
			count: 1,
			date: '2022-02-20',
			level: 1,
		},
		{
			count: 3,
			date: '2022-02-21',
			level: 2,
		},
		{
			count: 0,
			date: '2022-02-22',
			level: 0,
		},
		{
			count: 2,
			date: '2022-02-23',
			level: 1,
		},
		{
			count: 3,
			date: '2022-02-24',
			level: 2,
		},
		{
			count: 6,
			date: '2022-02-25',
			level: 3,
		},
		{
			count: 0,
			date: '2022-02-26',
			level: 0,
		},
		{
			count: 7,
			date: '2022-02-27',
			level: 3,
		},
		{
			count: 0,
			date: '2022-02-28',
			level: 0,
		},
		{
			count: 0,
			date: '2022-03-01',
			level: 0,
		},
		{
			count: 0,
			date: '2022-03-02',
			level: 0,
		},
		{
			count: 4,
			date: '2022-03-03',
			level: 2,
		},
		{
			count: 0,
			date: '2022-03-04',
			level: 0,
		},
		{
			count: 3,
			date: '2022-03-05',
			level: 2,
		},
		{
			count: 2,
			date: '2022-03-06',
			level: 1,
		},
		{
			count: 0,
			date: '2022-03-07',
			level: 0,
		},
		{
			count: 0,
			date: '2022-03-08',
			level: 0,
		},
		{
			count: 0,
			date: '2022-03-09',
			level: 0,
		},
		{
			count: 4,
			date: '2022-03-10',
			level: 2,
		},
		{
			count: 0,
			date: '2022-03-11',
			level: 0,
		},
		{
			count: 5,
			date: '2022-03-12',
			level: 2,
		},
		{
			count: 3,
			date: '2022-03-13',
			level: 2,
		},
		{
			count: 0,
			date: '2022-03-14',
			level: 0,
		},
		{
			count: 1,
			date: '2022-03-15',
			level: 1,
		},
		{
			count: 5,
			date: '2022-03-16',
			level: 2,
		},
		{
			count: 1,
			date: '2022-03-17',
			level: 1,
		},
		{
			count: 0,
			date: '2022-03-18',
			level: 0,
		},
		{
			count: 7,
			date: '2022-03-19',
			level: 3,
		},
		{
			count: 2,
			date: '2022-03-20',
			level: 1,
		},
		{
			count: 0,
			date: '2022-03-21',
			level: 0,
		},
		{
			count: 0,
			date: '2022-03-22',
			level: 0,
		},
		{
			count: 1,
			date: '2022-03-23',
			level: 1,
		},
		{
			count: 3,
			date: '2022-03-24',
			level: 2,
		},
		{
			count: 0,
			date: '2022-03-25',
			level: 0,
		},
		{
			count: 1,
			date: '2022-03-26',
			level: 1,
		},
		{
			count: 1,
			date: '2022-03-27',
			level: 1,
		},
		{
			count: 4,
			date: '2022-03-28',
			level: 2,
		},
		{
			count: 1,
			date: '2022-03-29',
			level: 1,
		},
		{
			count: 0,
			date: '2022-03-30',
			level: 0,
		},
		{
			count: 0,
			date: '2022-03-31',
			level: 0,
		},
		{
			count: 2,
			date: '2022-04-01',
			level: 1,
		},
		{
			count: 4,
			date: '2022-04-02',
			level: 2,
		},
		{
			count: 0,
			date: '2022-04-03',
			level: 0,
		},
		{
			count: 4,
			date: '2022-04-04',
			level: 2,
		},
		{
			count: 8,
			date: '2022-04-05',
			level: 4,
		},
		{
			count: 6,
			date: '2022-04-06',
			level: 3,
		},
		{
			count: 5,
			date: '2022-04-07',
			level: 2,
		},
		{
			count: 4,
			date: '2022-04-08',
			level: 2,
		},
		{
			count: 4,
			date: '2022-04-09',
			level: 2,
		},
		{
			count: 0,
			date: '2022-04-10',
			level: 0,
		},
		{
			count: 0,
			date: '2022-04-11',
			level: 0,
		},
		{
			count: 0,
			date: '2022-04-12',
			level: 0,
		},
		{
			count: 0,
			date: '2022-04-13',
			level: 0,
		},
		{
			count: 0,
			date: '2022-04-14',
			level: 0,
		},
		{
			count: 3,
			date: '2022-04-15',
			level: 2,
		},
		{
			count: 0,
			date: '2022-04-16',
			level: 0,
		},
		{
			count: 0,
			date: '2022-04-17',
			level: 0,
		},
		{
			count: 1,
			date: '2022-04-18',
			level: 1,
		},
		{
			count: 0,
			date: '2022-04-19',
			level: 0,
		},
		{
			count: 7,
			date: '2022-04-20',
			level: 3,
		},
		{
			count: 3,
			date: '2022-04-21',
			level: 2,
		},
		{
			count: 1,
			date: '2022-04-22',
			level: 1,
		},
		{
			count: 6,
			date: '2022-04-23',
			level: 3,
		},
		{
			count: 2,
			date: '2022-04-24',
			level: 1,
		},
		{
			count: 4,
			date: '2022-04-25',
			level: 2,
		},
		{
			count: 5,
			date: '2022-04-26',
			level: 2,
		},
		{
			count: 6,
			date: '2022-04-27',
			level: 3,
		},
		{
			count: 1,
			date: '2022-04-28',
			level: 1,
		},
		{
			count: 0,
			date: '2022-04-29',
			level: 0,
		},
		{
			count: 0,
			date: '2022-04-30',
			level: 0,
		},
		{
			count: 5,
			date: '2022-05-01',
			level: 2,
		},
		{
			count: 4,
			date: '2022-05-02',
			level: 2,
		},
		{
			count: 0,
			date: '2022-05-03',
			level: 0,
		},
		{
			count: 2,
			date: '2022-05-04',
			level: 1,
		},
		{
			count: 0,
			date: '2022-05-05',
			level: 0,
		},
		{
			count: 0,
			date: '2022-05-06',
			level: 0,
		},
		{
			count: 2,
			date: '2022-05-07',
			level: 1,
		},
		{
			count: 0,
			date: '2022-05-08',
			level: 0,
		},
		{
			count: 0,
			date: '2022-05-09',
			level: 0,
		},
		{
			count: 0,
			date: '2022-05-10',
			level: 0,
		},
		{
			count: 0,
			date: '2022-05-11',
			level: 0,
		},
		{
			count: 7,
			date: '2022-05-12',
			level: 3,
		},
		{
			count: 4,
			date: '2022-05-13',
			level: 2,
		},
		{
			count: 4,
			date: '2022-05-14',
			level: 2,
		},
		{
			count: 3,
			date: '2022-05-15',
			level: 2,
		},
		{
			count: 2,
			date: '2022-05-16',
			level: 1,
		},
		{
			count: 0,
			date: '2022-05-17',
			level: 0,
		},
		{
			count: 1,
			date: '2022-05-18',
			level: 1,
		},
		{
			count: 3,
			date: '2022-05-19',
			level: 2,
		},
		{
			count: 1,
			date: '2022-05-20',
			level: 1,
		},
		{
			count: 0,
			date: '2022-05-21',
			level: 0,
		},
		{
			count: 3,
			date: '2022-05-22',
			level: 2,
		},
		{
			count: 8,
			date: '2022-05-23',
			level: 4,
		},
		{
			count: 7,
			date: '2022-05-24',
			level: 3,
		},
		{
			count: 0,
			date: '2022-05-25',
			level: 0,
		},
		{
			count: 0,
			date: '2022-05-26',
			level: 0,
		},
		{
			count: 0,
			date: '2022-05-27',
			level: 0,
		},
		{
			count: 0,
			date: '2022-05-28',
			level: 0,
		},
		{
			count: 0,
			date: '2022-05-29',
			level: 0,
		},
		{
			count: 0,
			date: '2022-05-30',
			level: 0,
		},
		{
			count: 2,
			date: '2022-05-31',
			level: 1,
		},
		{
			count: 0,
			date: '2022-06-01',
			level: 0,
		},
		{
			count: 0,
			date: '2022-06-02',
			level: 0,
		},
		{
			count: 6,
			date: '2022-06-03',
			level: 3,
		},
		{
			count: 1,
			date: '2022-06-04',
			level: 1,
		},
		{
			count: 4,
			date: '2022-06-05',
			level: 2,
		},
		{
			count: 0,
			date: '2022-06-06',
			level: 0,
		},
		{
			count: 0,
			date: '2022-06-07',
			level: 0,
		},
		{
			count: 3,
			date: '2022-06-08',
			level: 2,
		},
		{
			count: 4,
			date: '2022-06-09',
			level: 2,
		},
		{
			count: 0,
			date: '2022-06-10',
			level: 0,
		},
		{
			count: 3,
			date: '2022-06-11',
			level: 2,
		},
		{
			count: 2,
			date: '2022-06-12',
			level: 1,
		},
		{
			count: 1,
			date: '2022-06-13',
			level: 1,
		},
		{
			count: 0,
			date: '2022-06-14',
			level: 0,
		},
		{
			count: 1,
			date: '2022-06-15',
			level: 1,
		},
		{
			count: 0,
			date: '2022-06-16',
			level: 0,
		},
		{
			count: 2,
			date: '2022-06-17',
			level: 1,
		},
		{
			count: 0,
			date: '2022-06-18',
			level: 0,
		},
		{
			count: 0,
			date: '2022-06-19',
			level: 0,
		},
		{
			count: 4,
			date: '2022-06-20',
			level: 2,
		},
		{
			count: 3,
			date: '2022-06-21',
			level: 2,
		},
		{
			count: 0,
			date: '2022-06-22',
			level: 0,
		},
		{
			count: 6,
			date: '2022-06-23',
			level: 3,
		},
		{
			count: 8,
			date: '2022-06-24',
			level: 4,
		},
		{
			count: 0,
			date: '2022-06-25',
			level: 0,
		},
		{
			count: 0,
			date: '2022-06-26',
			level: 0,
		},
		{
			count: 0,
			date: '2022-06-27',
			level: 0,
		},
		{
			count: 0,
			date: '2022-06-28',
			level: 0,
		},
		{
			count: 1,
			date: '2022-06-29',
			level: 1,
		},
		{
			count: 0,
			date: '2022-06-30',
			level: 0,
		},
		{
			count: 5,
			date: '2022-07-01',
			level: 2,
		},
		{
			count: 0,
			date: '2022-07-02',
			level: 0,
		},
		{
			count: 0,
			date: '2022-07-03',
			level: 0,
		},
		{
			count: 0,
			date: '2022-07-04',
			level: 0,
		},
		{
			count: 0,
			date: '2022-07-05',
			level: 0,
		},
		{
			count: 4,
			date: '2022-07-06',
			level: 2,
		},
		{
			count: 0,
			date: '2022-07-07',
			level: 0,
		},
		{
			count: 3,
			date: '2022-07-08',
			level: 2,
		},
		{
			count: 0,
			date: '2022-07-09',
			level: 0,
		},
		{
			count: 0,
			date: '2022-07-10',
			level: 0,
		},
		{
			count: 6,
			date: '2022-07-11',
			level: 3,
		},
		{
			count: 0,
			date: '2022-07-12',
			level: 0,
		},
		{
			count: 2,
			date: '2022-07-13',
			level: 1,
		},
		{
			count: 3,
			date: '2022-07-14',
			level: 2,
		},
		{
			count: 6,
			date: '2022-07-15',
			level: 3,
		},
		{
			count: 0,
			date: '2022-07-16',
			level: 0,
		},
		{
			count: 0,
			date: '2022-07-17',
			level: 0,
		},
		{
			count: 1,
			date: '2022-07-18',
			level: 1,
		},
		{
			count: 8,
			date: '2022-07-19',
			level: 4,
		},
		{
			count: 4,
			date: '2022-07-20',
			level: 2,
		},
		{
			count: 0,
			date: '2022-07-21',
			level: 0,
		},
		{
			count: 0,
			date: '2022-07-22',
			level: 0,
		},
		{
			count: 9,
			date: '2022-07-23',
			level: 4,
		},
		{
			count: 0,
			date: '2022-07-24',
			level: 0,
		},
		{
			count: 0,
			date: '2022-07-25',
			level: 0,
		},
		{
			count: 0,
			date: '2022-07-26',
			level: 0,
		},
		{
			count: 5,
			date: '2022-07-27',
			level: 2,
		},
		{
			count: 2,
			date: '2022-07-28',
			level: 1,
		},
		{
			count: 4,
			date: '2022-07-29',
			level: 2,
		},
		{
			count: 4,
			date: '2022-07-30',
			level: 2,
		},
		{
			count: 4,
			date: '2022-07-31',
			level: 2,
		},
		{
			count: 3,
			date: '2022-08-01',
			level: 2,
		},
		{
			count: 2,
			date: '2022-08-02',
			level: 1,
		},
		{
			count: 5,
			date: '2022-08-03',
			level: 2,
		},
		{
			count: 2,
			date: '2022-08-04',
			level: 1,
		},
		{
			count: 4,
			date: '2022-08-05',
			level: 2,
		},
		{
			count: 3,
			date: '2022-08-06',
			level: 2,
		},
		{
			count: 5,
			date: '2022-08-07',
			level: 2,
		},
		{
			count: 6,
			date: '2022-08-08',
			level: 3,
		},
		{
			count: 3,
			date: '2022-08-09',
			level: 2,
		},
		{
			count: 0,
			date: '2022-08-10',
			level: 0,
		},
		{
			count: 4,
			date: '2022-08-11',
			level: 2,
		},
		{
			count: 0,
			date: '2022-08-12',
			level: 0,
		},
		{
			count: 7,
			date: '2022-08-13',
			level: 3,
		},
		{
			count: 3,
			date: '2022-08-14',
			level: 2,
		},
		{
			count: 0,
			date: '2022-08-15',
			level: 0,
		},
		{
			count: 2,
			date: '2022-08-16',
			level: 1,
		},
		{
			count: 5,
			date: '2022-08-17',
			level: 2,
		},
		{
			count: 6,
			date: '2022-08-18',
			level: 3,
		},
		{
			count: 0,
			date: '2022-08-19',
			level: 0,
		},
		{
			count: 2,
			date: '2022-08-20',
			level: 1,
		},
		{
			count: 5,
			date: '2022-08-21',
			level: 2,
		},
		{
			count: 4,
			date: '2022-08-22',
			level: 2,
		},
		{
			count: 0,
			date: '2022-08-23',
			level: 0,
		},
		{
			count: 0,
			date: '2022-08-24',
			level: 0,
		},
		{
			count: 3,
			date: '2022-08-25',
			level: 2,
		},
		{
			count: 7,
			date: '2022-08-26',
			level: 3,
		},
		{
			count: 3,
			date: '2022-08-27',
			level: 2,
		},
		{
			count: 7,
			date: '2022-08-28',
			level: 3,
		},
		{
			count: 0,
			date: '2022-08-29',
			level: 0,
		},
		{
			count: 2,
			date: '2022-08-30',
			level: 1,
		},
		{
			count: 8,
			date: '2022-08-31',
			level: 4,
		},
		{
			count: 2,
			date: '2022-09-01',
			level: 1,
		},
		{
			count: 2,
			date: '2022-09-02',
			level: 1,
		},
		{
			count: 5,
			date: '2022-09-03',
			level: 2,
		},
		{
			count: 1,
			date: '2022-09-04',
			level: 1,
		},
		{
			count: 0,
			date: '2022-09-05',
			level: 0,
		},
		{
			count: 0,
			date: '2022-09-06',
			level: 0,
		},
		{
			count: 3,
			date: '2022-09-07',
			level: 2,
		},
		{
			count: 0,
			date: '2022-09-08',
			level: 0,
		},
		{
			count: 0,
			date: '2022-09-09',
			level: 0,
		},
		{
			count: 0,
			date: '2022-09-10',
			level: 0,
		},
		{
			count: 4,
			date: '2022-09-11',
			level: 2,
		},
		{
			count: 2,
			date: '2022-09-12',
			level: 1,
		},
		{
			count: 5,
			date: '2022-09-13',
			level: 2,
		},
		{
			count: 6,
			date: '2022-09-14',
			level: 3,
		},
		{
			count: 0,
			date: '2022-09-15',
			level: 0,
		},
		{
			count: 0,
			date: '2022-09-16',
			level: 0,
		},
		{
			count: 5,
			date: '2022-09-17',
			level: 2,
		},
		{
			count: 0,
			date: '2022-09-18',
			level: 0,
		},
		{
			count: 0,
			date: '2022-09-19',
			level: 0,
		},
		{
			count: 0,
			date: '2022-09-20',
			level: 0,
		},
		{
			count: 2,
			date: '2022-09-21',
			level: 1,
		},
		{
			count: 0,
			date: '2022-09-22',
			level: 0,
		},
		{
			count: 3,
			date: '2022-09-23',
			level: 2,
		},
		{
			count: 0,
			date: '2022-09-24',
			level: 0,
		},
		{
			count: 6,
			date: '2022-09-25',
			level: 3,
		},
		{
			count: 0,
			date: '2022-09-26',
			level: 0,
		},
		{
			count: 0,
			date: '2022-09-27',
			level: 0,
		},
		{
			count: 3,
			date: '2022-09-28',
			level: 2,
		},
		{
			count: 3,
			date: '2022-09-29',
			level: 2,
		},
		{
			count: 0,
			date: '2022-09-30',
			level: 0,
		},
		{
			count: 0,
			date: '2022-10-01',
			level: 0,
		},
		{
			count: 0,
			date: '2022-10-02',
			level: 0,
		},
		{
			count: 0,
			date: '2022-10-03',
			level: 0,
		},
		{
			count: 3,
			date: '2022-10-04',
			level: 2,
		},
		{
			count: 0,
			date: '2022-10-05',
			level: 0,
		},
		{
			count: 0,
			date: '2022-10-06',
			level: 0,
		},
		{
			count: 9,
			date: '2022-10-07',
			level: 4,
		},
		{
			count: 7,
			date: '2022-10-08',
			level: 3,
		},
		{
			count: 0,
			date: '2022-10-09',
			level: 0,
		},
		{
			count: 0,
			date: '2022-10-10',
			level: 0,
		},
		{
			count: 1,
			date: '2022-10-11',
			level: 1,
		},
		{
			count: 6,
			date: '2022-10-12',
			level: 3,
		},
		{
			count: 0,
			date: '2022-10-13',
			level: 0,
		},
		{
			count: 1,
			date: '2022-10-14',
			level: 1,
		},
		{
			count: 0,
			date: '2022-10-15',
			level: 0,
		},
		{
			count: 1,
			date: '2022-10-16',
			level: 1,
		},
		{
			count: 9,
			date: '2022-10-17',
			level: 4,
		},
		{
			count: 7,
			date: '2022-10-18',
			level: 3,
		},
		{
			count: 0,
			date: '2022-10-19',
			level: 0,
		},
		{
			count: 0,
			date: '2022-10-20',
			level: 0,
		},
		{
			count: 0,
			date: '2022-10-21',
			level: 0,
		},
		{
			count: 0,
			date: '2022-10-22',
			level: 0,
		},
		{
			count: 0,
			date: '2022-10-23',
			level: 0,
		},
		{
			count: 0,
			date: '2022-10-24',
			level: 0,
		},
		{
			count: 0,
			date: '2022-10-25',
			level: 0,
		},
		{
			count: 0,
			date: '2022-10-26',
			level: 0,
		},
		{
			count: 0,
			date: '2022-10-27',
			level: 0,
		},
		{
			count: 0,
			date: '2022-10-28',
			level: 0,
		},
		{
			count: 0,
			date: '2022-10-29',
			level: 0,
		},
		{
			count: 1,
			date: '2022-10-30',
			level: 1,
		},
		{
			count: 0,
			date: '2022-10-31',
			level: 0,
		},
		{
			count: 1,
			date: '2022-11-01',
			level: 1,
		},
		{
			count: 3,
			date: '2022-11-02',
			level: 2,
		},
		{
			count: 6,
			date: '2022-11-03',
			level: 3,
		},
		{
			count: 4,
			date: '2022-11-04',
			level: 2,
		},
		{
			count: 0,
			date: '2022-11-05',
			level: 0,
		},
		{
			count: 0,
			date: '2022-11-06',
			level: 0,
		},
		{
			count: 3,
			date: '2022-11-07',
			level: 2,
		},
		{
			count: 3,
			date: '2022-11-08',
			level: 2,
		},
		{
			count: 0,
			date: '2022-11-09',
			level: 0,
		},
		{
			count: 1,
			date: '2022-11-10',
			level: 1,
		},
		{
			count: 6,
			date: '2022-11-11',
			level: 3,
		},
		{
			count: 0,
			date: '2022-11-12',
			level: 0,
		},
		{
			count: 3,
			date: '2022-11-13',
			level: 2,
		},
		{
			count: 1,
			date: '2022-11-14',
			level: 1,
		},
		{
			count: 3,
			date: '2022-11-15',
			level: 2,
		},
		{
			count: 0,
			date: '2022-11-16',
			level: 0,
		},
		{
			count: 0,
			date: '2022-11-17',
			level: 0,
		},
		{
			count: 0,
			date: '2022-11-18',
			level: 0,
		},
		{
			count: 2,
			date: '2022-11-19',
			level: 1,
		},
		{
			count: 3,
			date: '2022-11-20',
			level: 2,
		},
		{
			count: 1,
			date: '2022-11-21',
			level: 1,
		},
		{
			count: 5,
			date: '2022-11-22',
			level: 2,
		},
		{
			count: 0,
			date: '2022-11-23',
			level: 0,
		},
		{
			count: 0,
			date: '2022-11-24',
			level: 0,
		},
		{
			count: 2,
			date: '2022-11-25',
			level: 1,
		},
		{
			count: 2,
			date: '2022-11-26',
			level: 1,
		},
		{
			count: 1,
			date: '2022-11-27',
			level: 1,
		},
		{
			count: 0,
			date: '2022-11-28',
			level: 0,
		},
		{
			count: 4,
			date: '2022-11-29',
			level: 2,
		},
		{
			count: 6,
			date: '2022-11-30',
			level: 3,
		},
		{
			count: 0,
			date: '2022-12-01',
			level: 0,
		},
		{
			count: 1,
			date: '2022-12-02',
			level: 1,
		},
		{
			count: 1,
			date: '2022-12-03',
			level: 1,
		},
		{
			count: 0,
			date: '2022-12-04',
			level: 0,
		},
		{
			count: 2,
			date: '2022-12-05',
			level: 1,
		},
		{
			count: 2,
			date: '2022-12-06',
			level: 1,
		},
		{
			count: 0,
			date: '2022-12-07',
			level: 0,
		},
		{
			count: 0,
			date: '2022-12-08',
			level: 0,
		},
		{
			count: 1,
			date: '2022-12-09',
			level: 1,
		},
		{
			count: 0,
			date: '2022-12-10',
			level: 0,
		},
		{
			count: 0,
			date: '2022-12-11',
			level: 0,
		},
		{
			count: 0,
			date: '2022-12-12',
			level: 0,
		},
		{
			count: 0,
			date: '2022-12-13',
			level: 0,
		},
		{
			count: 6,
			date: '2022-12-14',
			level: 3,
		},
		{
			count: 0,
			date: '2022-12-15',
			level: 0,
		},
		{
			count: 2,
			date: '2022-12-16',
			level: 1,
		},
		{
			count: 0,
			date: '2022-12-17',
			level: 0,
		},
		{
			count: 0,
			date: '2022-12-18',
			level: 0,
		},
		{
			count: 0,
			date: '2022-12-19',
			level: 0,
		},
		{
			count: 1,
			date: '2022-12-20',
			level: 1,
		},
		{
			count: 4,
			date: '2022-12-21',
			level: 2,
		},
		{
			count: 0,
			date: '2022-12-22',
			level: 0,
		},
		{
			count: 3,
			date: '2022-12-23',
			level: 2,
		},
		{
			count: 4,
			date: '2022-12-24',
			level: 2,
		},
		{
			count: 1,
			date: '2022-12-25',
			level: 1,
		},
		{
			count: 1,
			date: '2022-12-26',
			level: 1,
		},
		{
			count: 8,
			date: '2022-12-27',
			level: 4,
		},
		{
			count: 2,
			date: '2022-12-28',
			level: 1,
		},
		{
			count: 0,
			date: '2022-12-29',
			level: 0,
		},
		{
			count: 0,
			date: '2022-12-30',
			level: 0,
		},
		{
			count: 0,
			date: '2022-12-31',
			level: 0,
		},
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

-   [React Activity Calendar](https://www.npmjs.com/package/react-activity-calendar)
