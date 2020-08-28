import React, { Component } from "react";
import Menu from "../menu/menu";
import './index.css';

export default class Index extends Component {


    render(){
        return (
            
            <div className="mainDiv">
               <div className="menu">
               <Menu />
                </div>
               <div className="pages">
                    Home
               </div>
            </div>

        )
    }
}