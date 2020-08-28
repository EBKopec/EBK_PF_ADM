import React, { Component } from "react";
import Select from 'react-select';
import Menu from "../../menu/menu";
import { Tab, Tabs } from '@material-ui/core';
import Table from '../../../utils/table/table';
import Data from "../../../services/api";
import { Form, Container } from "./styles";

const columns = "TIPO.ORIGEM.DATA.HORA.DESTINO.CIDADE_DESTINO.DURACAO_REAL.CUSTO.VALIDAR_AGRUPAMENTO.VALIDAR_HORA";
const heads = ["TIPO",
    "ORIGEM",
    "DATA",
    "HORA",
    "DESTINO",
    "CIDADE DESTINO",
    "DURAÇÃO",
    "CUSTO - R$ ",
    "CHECK_GRUPO",
    "CHECK_HORA"
]

export default class showBilling extends Component {
    constructor() {
        super()
        this.state = {
            content: [],
            contentInfo: {},
            page: 1,
            pages: 1,
            tabIndex: 0,
            selectedTab: 0,
            year: null,
            month: null,
            selectedYear: new Date().getFullYear(),
            selectedMonth: parseInt(new Date().getMonth()) + 1,
            // download: null,
            selectedOption: null,
        }
    }

    componentDidMount() {
        this.loadContent();
        this.loadYearMonth();
    }

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


    loadContent = async (page = 1) => {
        const { selectedYear, selectedMonth } = this.state
        try {
            const route = this.state.selectedTab === null ? null : this.state.selectedTab;
            const YM = (this.state.selectedYear.value && this.state.selectedMonth.value) === undefined ? `${selectedYear}${selectedMonth}` : `${this.state.selectedYear.value}${this.state.selectedMonth.value}`
            const data = await Data.get(`/faturamento/${route}/${YM}/${page}`);
            const { docs, ...contentInfo } = data.data
            this.setState({ content: docs, contentInfo, page, route });
        } catch (error) {
            console.log(error);
        }

    };

    // Year Selected
    yearChange = selectedYear => {
        this.setState({ selectedYear });
        // console.log(`Year Selected: `, selectedYear.value);
    };
    // Month Selected
    monthChange = selectedMonth => {
        this.setState({ selectedMonth });
        // console.log(`Month Selected: `, selectedMonth.value);
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

    handleChange = async (event, newValue) => {
        const { selectedYear, selectedMonth } = this.state;
        try {
            const page = 1;
            const value = newValue;
            const post = await Data.get(`/faturamento/${value}/${selectedYear.value}${selectedMonth.value}/${page}`);
            const { docs, ...contentInfo } = post.data
            this.setState({ selectedTab: value, content: docs, contentInfo, pages: contentInfo.Pages.Pages, page });
        } catch (error) {
            console.log(error);
        }
    };

    handleSubmit = async e => {
        const { selectedYear, selectedMonth, selectedTab, page } = this.state;

        const response = await Data.get(`/faturamento/${selectedTab}/${selectedYear.value}${selectedMonth.value}/${page}`);
        // console.log("Pages", response);
        const { docs, ...contentInfo } = response.data;
        // console.log(docs);
        this.setState({ selectedTab, content: docs, pages: contentInfo.Pages.Pages, page });
        // this.download();
        // console.log(response);
    }

    handleSubmitDownload = async (e) => {
        e.preventDefault();
        const { selectedYear, selectedMonth, selectedOption } = this.state;
        console.log(selectedYear, selectedMonth)
        if (!selectedYear || !selectedMonth || !selectedOption) {
            alert("Escolha um formato para download!");
        } else {
            const year = String(selectedYear.value);
            const month = String(selectedMonth.value);
            try {
                Data({
                    url: `/download/${year}${month}&${selectedOption}`, //your url
                    method: 'GET',
                    responseType: 'blob', // important
                }).then((response) => {
                    const url = window.URL.createObjectURL(new Blob([response.data]));
                    const link = document.createElement('a');
                    link.href = url;
                    link.setAttribute('download', `Files_${year}${month}.zip`); //or any other extension
                    document.body.appendChild(link);
                    link.click();
                });

            } catch (err) {
                console.log(err);
            }
        }
    }

    // handle action on radio button
    handleOptionChange = changeEvent => {
        let event = null;
        console.log(this.state.selectedOption);
        // console.log('Evento', changeEvent.target.value);
        event = changeEvent.target.value;
        // console.log('Event', event)

        this.setState({ selectedOption: event });
    }

    // download = () => {
    //     const { selectedOption } = this.state;
    //     const download = (

    //         <div className="radio">
    //             <Container>
    //                 <Form onSubmit={this.handleSubmitDownload}>
    //                     <input
    //                         id="XLSX"
    //                         type="radio"
    //                         className="radio"
    //                         name="radioExcel"
    //                         value="XLSX"
    //                         checked={selectedOption === "XLSX"}
    //                         onChange={this.handleOptionChange} />
    //                     <label for="XLSX">Excel</label>
    //                     <input
    //                         id="PDF"
    //                         name="radioPdf"
    //                         className="radio"
    //                         type="radio"
    //                         value="PDF"
    //                         checked={selectedOption === "PDF"}
    //                         onChange={this.handleOptionChange} />
    //                     <label for="PDF">PDF</label>
    //                     <button type="submit">Download</button>
    //                 </Form>
    //             </Container>
    //         </div>
    //     )
    //     this.setState({ download })
    // }

    showBilling = () => {
        const { content, page, pages } = this.state;
        const showBilling = (
            <div className="groups">
                <Tabs className="tabs" onChange={this.handleChange} value={this.state.selectedTab}>
                    <Tab className={this.state.selectedTab === 0 ? "activated" : "tab"} label="PMPG" />
                    <Tab className={this.state.selectedTab === 1 ? "activated" : "tab"} label="PMPG 0800" />
                    <Tab className={this.state.selectedTab === 2 ? "activated" : "tab"} label="SME ESCOLA" />
                    <Tab className={this.state.selectedTab === 3 ? "activated" : "tab"} label="SME CMEI" />
                    <Tab className={this.state.selectedTab === 4 ? "activated" : "tab"} label="FMS PAB" />
                    <Tab className={this.state.selectedTab === 5 ? "activated" : "tab"} label="FMS PAB 0800" />
                    <Tab className={this.state.selectedTab === 6 ? "activated" : "tab"} label="FMS AIH" />
                    <Tab className={this.state.selectedTab === 7 ? "activated" : "tab"} label="FMS AIH 0800" />
                </Tabs>
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
        return showBilling;
    }

    render() {
        const { selectedYear, selectedMonth, year, month, selectedOption } = this.state;
        return (
            <div className="mainDiv">
                <div className="menu">
                    <Menu />
                </div>
                <h1>Pesquisar Faturamento</h1>
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
                    
                    <Container>
                        <Form onSubmit={this.handleSubmitDownload}>
                        <div className="radio">
                            <input
                                id="XLSX"
                                type="radio"
                                className="radio"
                                name="radioExcel"
                                value="XLSX"
                                checked={selectedOption === "XLSX"}
                                onChange={this.handleOptionChange} />
                            <label for="XLSX">Excel</label>
                            <input
                                id="PDF"
                                name="radioPdf"
                                className="radio"
                                type="radio"
                                value="PDF"
                                checked={selectedOption === "PDF"}
                                onChange={this.handleOptionChange} />
                            <label for="PDF">PDF</label>
                            </div>
                            <button type="submit">Download</button>
                        </Form>
                    </Container>
                    
                    
                

                {this.showBilling()}
            </div>
        )
    }




}