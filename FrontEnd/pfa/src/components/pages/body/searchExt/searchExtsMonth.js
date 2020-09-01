import React, { Component } from "react";
import Select from 'react-select';
import Menu from "../../menu/menu";
import Table from '../../../utils/table/table';
import Data from "../../../services/api";
import { checkArray } from '../../../utils/bytes'; 

const columns = "linha.Grupo.ATIVADOS_MES.DESCONECTADOS.EM_ATIVACAO";
const heads = [ 
    "LINHA",   
    "GRUPO",
    "DATA ATIVAÇÃO",
    "DATA DESCONEXÃO",
    "DATA CADASTRO EM ATIVAÇÃO"
]

export default class SearchExtsMonth extends Component {
    constructor() {
        super();
        this.state = {
            content: [],
            contentInfo: {},
            page: 1,
            pages: 1,
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

    loadContent = async (page = 1) => {
        const { selectedYear, selectedMonth } = this.state
        try {
            const YM = (this.state.selectedYear.value && this.state.selectedMonth.value) === undefined ? `${selectedYear}${selectedMonth}` : `${this.state.selectedYear.value}${this.state.selectedMonth.value}`
            const data = await Data.get(`/extensions/desc/${YM}/${page}`);
            const { docs, ...contentInfo } = data.data
            this.setState({ content: docs, contentInfo, page });
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
        const { selectedYear, selectedMonth, page} = this.state
        const YM = (this.state.selectedYear.value && this.state.selectedMonth.value) === undefined ? `${selectedYear}${selectedMonth}` : `${this.state.selectedYear.value}${this.state.selectedMonth.value}`
        const response = await Data.get(`/extensions/desc/${YM}/${page}`);
        const { docs, ...contentInfo } = response.data;
        try {
            checkArray(docs)
        } catch (error) {
            console.log(error);
            return alert(`Não há ramais para o mês de ${selectedMonth.label} de ${selectedYear.value}!`);
        }
        this.setState({ content: docs, pages: contentInfo.Pages.Pages, page  });
    }

    showExts = () => {
        const { content, page, pages } = this.state;
        console.log('Content', content);
        const showExts = (
            <div className="groupsExt">
                <div className="table">
                    <Table Header={heads} data={content} columns={columns} />
                </div>
                <div className="actions">
                    <button disabled={page <= 1} onClick={this.firstPage}>Primeira Página</button>
                    <button disabled={page <= 1} onClick={this.prevPage}>Anterior</button>
                    <button disabled={true}>Página {page} de {pages}</button>
                    <input placeholder="Insira a Página" name="page" ref="newPage" />
                    <button onClick={this.findPage}>Buscar</button>
                    <button disabled={page >= pages} onClick={this.nextPage}>Próximo</button>
                    <button disabled={page >= pages} onClick={this.lastPage}>Última Página</button>
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

    prevPage = () => {
        const { page } = this.state;
        //contentInfo
        if (page <= 1) return;
        const pageNumber = page - 1;
        // console.log(`Current Page: ${page}, Previous Page ${pageNumber}`)
        this.loadContent(pageNumber);

    };
    nextPage = () => {
        const { page, pages } = this.state;
        if (page >= pages) return;
        const pageNumber = page + 1;
        // console.log(`Current Page: ${page}, Next Page: ${pageNumber}`);
        this.loadContent(pageNumber);
    };

    firstPage = () => {
        const { page } = this.state;
        if (page <= 1) return;
        const pageNumber = 1;
        this.loadContent(pageNumber);
    }

    lastPage = () => {
        const { page, pages } = this.state;
        // console.log('Last Page:', pages);
        if (page >= pages) return;
        this.loadContent(pages);
    };

    findPage = () => {
        const { contentInfo } = this.state;
        if ((this.refs.newPage.value < 1) || (this.refs.newPage.value > contentInfo.Pages.Pages)) {
            alert('A página solicitada não existe. Favor corrigir sua busca.');
            return;
        }
        const page = this.refs.newPage.value;
        this.loadContent(parseInt(page));
    };

    loadYearMonth = async () => {
        let ano = [];
        let mes = [];
        // const { selectedYear, year } = this.state;
        const resp_Y = await Data.get(`/ano`);
        const resp_M = await Data.get(`/mes`);
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
                <h1>Mostrar Ramais Mês</h1>
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