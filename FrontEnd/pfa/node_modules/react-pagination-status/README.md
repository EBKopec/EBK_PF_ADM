# react-pagination-status

[![Build Status](https://travis-ci.org/addhome2001/react-pagination-status.svg?branch=master)](https://travis-ci.org/addhome2001/react-pagination-status)

[![Known Vulnerabilities](https://snyk.io/test/github/addhome2001/react-pagination-status/badge.svg)](https://snyk.io/test/github/addhome2001/react-pagination-status)

> A pagination component of React let you to manage page status.

If you want use `react-pagination-status` with table component, maybe you can try [this](https://www.npmjs.com/package/react-pagination-table)

## Install
```js
 npm install --save react-pagination-status
```

## Migration
After the version `2.x`, the behavior of the `className` prop will be a little different. For a better way to architect your CSS, the className of the specific components will be more maintainable. Such as the className of the buttons will become `{prefixClassName}__btn`, and the activated button will be `{prefixClassName}__btn--active`.

> If you want to see more `CSS`. The [example](https://github.com/addhome2001/react-pagination-status/blob/master/example) will be helpful to you.

## Usage

### [Demo]( https://addhome2001.github.io/react-pagination-status/)

````javascript
import React from 'react';
import Pagination from 'react-pagination-status';

export default class app extends React.Component {

    constructor(props) {
        super(props);
        this.handleChangePage = ::this.handleChangePage;
        //Store activePage state into parent component
        this.state = {
            activePage: 0
        }
    }

    handleChangePage(page) {
        this.setState({
            activePage: page
        })
    }

    render() {
        const { activePage } = this.state;
        return (
            <div>
                <div>now page number: { activePage +1 }</div>
                <Pagination
                    handleChangePage = { this.handleChangePage }
                    activePage = { activePage }
                    totalCount = { 10 }
                    perPageItemCount = { 2 }
                />
            </div>
        )
    }
}
````

## className
The `react-pagination-status` is the default **className** and **prefix**. You can pass custom name with the `className` prop.

> In addition, setting the specific components to the differences styles and status by these **className**
>- {**className**}__item(the `<li>` tags)
>- {**className**}__btn(the page button)
>- {**className**}__btn--active(the activated page button)
>- {**className**}__btn--disable

## API

### Pagination

| Props        | Description                        | Type          | Default                  |
|------------------|------------------------------------|---------------|--------------------------|
| handleChangePage   |  the argument is current page          | function      | isRequired                      |
| activePage          | the activated page                       | Number        | isRequired                |
| totalCount            | the length of the items                 | Number        | isRequired                       |
| perPageItemCount  | the numbers of the items on per page           | Number        | isRequired                       |
| nextPageText         | the text of `nextPage` button                     | String        | 下一頁                    |
| prePageText         | the text of `previousPage` button                     | String        | 上一頁                    |
| className         | the default className                    | String        | react-pagination-status                   |
| partialPageCount         | the numbers of the page buttons                     | Number        | 5                  |




## Example
```
npm start
```

By default, the example is on the `8000` port after run the command above. Then you can access `localhost:8000` to see the demo.

## Test
```
npm test
```

LICENSE
=======

MIT
