import React, { Component } from "react";
import Select from 'react-select';



class SelectField extends Component {

    render() {
        return (
            <div className="selected">
                <Select
                    className="selected"
                    value={this.props.value}
                    onChange={(e) => this.props.onChange(e.target.value)}
                    options={this.props.options}
                    placeholder={this.props.placeholder}
                    isSearchable />
            </div>
        )
    }
}

export default SelectField;