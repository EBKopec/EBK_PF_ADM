import React, { Component } from "react";
import Menu from "../../menu/menu";



export default class BackupBilling extends Component {


    render() {
        return (
            <div className="mainDiv">
                <div className="menu">
                    <Menu />
                </div>
                <div className="backupFaturamento">
                    Backup Faturamento
                </div>
            </div>

        )
    }
}