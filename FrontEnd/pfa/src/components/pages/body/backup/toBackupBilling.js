import React, { Component } from "react";
import Menu from "../../menu/menu";



export default class ToBackupBilling extends Component {


    render() {
        return (
            <div className="mainDiv">
                <div className="menu">
                    <Menu />
                </div>
                <div className="toBackupFaturamento">
                    Backups à Realizar
                </div>
            </div>

        )
    }
}