import React, { Component } from "react";
import Select from 'react-select';
import Menu from "../../menu/menu";
import Table from '../../../utils/table/table';
import Data from "../../../services/api";

const columns = "Grupo.RAMAIS_ATIVOS.ATIVADOS_MES.EM_ATIVACAO.DESCONECTADOS";
const heads = [ 
    "GRUPO",
    "RAMAIS ATIVOS",
    "RAMAIS ATIVADOS NO MÊS ATUAL",
    "RAMAIS EM ATIVAÇÃO",
    "RAMAIS DESCONECTADOS"
]

export default class SearchExts extends Component {
    constructor() {
        super();
        this.state = {
            content: [],
            year: null,
            month: null,
            selectedYear: new Date().getFullYear(),
            selectedMonth: parseInt(new Date().getMonth()) + 1
        }
    }
    componentDidMount() {
        this.loadContent();
        this.loadYearMonth();
    }

    loadContent = async () => {
        const { selectedYear, selectedMonth } = this.state
        try {
            const YM = (this.state.selectedYear.value && this.state.selectedMonth.value) === undefined ? `${selectedYear}${selectedMonth}` : `${this.state.selectedYear.value}${this.state.selectedMonth.value}`
            const response = await Data.get(`/extensions/qty/${YM}`);
            const { data } = response
            this.setState({ content: data });
        } catch (error) {
            console.log(error);
        }
    };

    loadYearMonth = async () => {
        let ano = [];
        let mes = [];
        const resp_Y = await Data.get(`/ano`);
        const resp_M = await Data.get(`/mes`);
        ano = resp_Y.data.map((id_ano) => { return { value: id_ano.id_ano, label: id_ano.id_ano } });
        mes = resp_M.data.map((id_mes) => { return { value: id_mes.id_mes, label: id_mes.mes } });
        this.setState({ year: ano, month: mes });
    }

    handleSubmit = async () => {
        const { selectedYear, selectedMonth} = this.state
        try {
            const YM = (this.state.selectedYear.value && this.state.selectedMonth.value) === undefined ? `${selectedYear}${selectedMonth}` : `${this.state.selectedYear.value}${this.state.selectedMonth.value}`
            const response = await Data.get(`/extensions/qty/${YM}`);
            const { data } = response;
            this.setState({ content: data});
        } catch (error) {
            console.log(error);
        }
    }

    showExts = () => {
        const { content} = this.state;
        console.log('Content', content);
        const showExts = (
            <div className="groupsExt">
                <div className="table">
                    <Table Header={heads} data={content} columns={columns} />
                </div>
            </div>
        )
        return showExts;
    }


    // Year Selected
    yearChange = selectedYear => {
        this.setState({ selectedYear });
        console.log(`Year Selected: `, selectedYear.value);
    };
    // Month Selected
    monthChange = selectedMonth => {
        this.setState({ selectedMonth });
        console.log(`Month Selected: `, selectedMonth.value);
    };

    loadYearMonth = async () => {
        let ano = [];
        let mes = [];
        // const { selectedYear, year } = this.state;
        const resp_Y = await Data.get(`/ano`);
        const resp_M = await Data.get(`/mes`);
        // console.log('YM',resp_Y,resp_M)
        ano = resp_Y.data.map((id_ano) => { return { value: id_ano.id_ano, label: id_ano.id_ano } });
        mes = resp_M.data.map((id_mes) => { return { value: id_mes.id_mes, label: id_mes.mes } });
        // console.log("Years", ano);
        this.setState({ year: ano, month: mes });
    }

    render() {
        const { selectedYear, selectedMonth, year, month } = this.state;
        // console.log("Content", content);
        return (
            <div className="mainDiv">
                <div className="menu">
                    <Menu />
                </div>
                <h1>Mostrar Ramais Quantidade Mês</h1>
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
                    <button className="findButton" onClick={this.handleSubmit}>Pesquisar</button>
                </div>

                 {this.showExts()}
            </div>

        )
    }
}