import React, { Component } from "react";
import Menu from "../../menu/menu";
import Select from 'react-select';
import api from "../../../services/api";
// import ShowBilling from "./showBilling";
import "./styles.css";



export default class MainFunction extends Component {
    constructor(props) {
        super(props);
        this.state = {
            year: null,
            month: null,
            selectedYear: null,
            selectedMonth: null,
        }
    }

    handleSubmit = async e => {
        const { selectedYear, selectedMonth } = this.state;
        await api.get(`/pmpg/${selectedYear.value}${selectedMonth.value}`);
        this.setState({selectedYear: null, selectedMonth: null });
        // console.log(response);
    }


    async componentDidMount() {
        // console.log(this.state)
        this.loadYearMonth();
        // let ano = [];
        // let mes = [];
        // // const { selectedYear, year } = this.state;
        // const resp_Y = await api.get(`/ano`);
        // const resp_M = await api.get(`/mes`);
        // ano = resp_Y.data.map((id_ano) => {return {value: id_ano.id_ano, label:id_ano.id_ano }});
        // mes = resp_M.data.map((id_mes) => {return {value: id_mes.id_mes, label:id_mes.mes}});
        // // console.log("Years", ano);
        // this.setState({ year: ano, month: mes });
    }

    loadYearMonth = async () => {
        let ano = [];
        let mes = [];
        // const { selectedYear, year } = this.state;
        const resp_Y = await api.get(`/ano`);
        const resp_M = await api.get(`/mes`);
        ano = resp_Y.data.map((id_ano) => { return { value: id_ano.id_ano, label: id_ano.id_ano } });
        mes = resp_M.data.map((id_mes) => { return { value: id_mes.id_mes, label: id_mes.mes } });
        // console.log("Years", ano);
        this.setState({ year: ano, month: mes });
    }

    yearChange = selectedYear => {
        this.setState({ selectedYear });
        console.log(`Year Selected: `, selectedYear.value);
    };
    monthChange = selectedMonth => {
        this.setState({ selectedMonth });
        console.log(`Month Selected: `, selectedMonth.value);
    };

    render() {
        const { selectedYear, selectedMonth, year, month } = this.state;
        // console.log("props", ShowBilling)
        return (
            <div className="main">
                <div className="menu">
                    <Menu />
                </div>
                <h1>Executar/Pesquisar Faturamento</h1>
                <div className="finders">
                    <Select
                        className="selected"
                        value={selectedYear}
                        onChange={this.yearChange}
                        options={year}
                        placeholder="Selecione o Ano"
                        isSearchable />

                    <Select
                        className="selected"
                        value={selectedMonth}
                        onChange={this.monthChange}
                        options={month}
                        placeholder="Selecione o Mês"
                        isSearchable />
                    <button className="findButton" onClick={this.handleSubmit}>Executar Faturamento</button>
                </div>
            </div>

        )
    }
}