import React, { Component } from "react";
import Menu from "../../menu/menu";
import Select from 'react-select';
import Table from '../../../utils/table/table';
import Group from '../../../utils/groups.json';
import api from "../../../services/api";
import { checkArray } from '../../../utils/bytes'; 
// import { Form, Container } from "./styles";

const columns = "USER_CODE.GRUPO.CALL_TYPE.COST.MIN_TELEPHONE_FRANCHISE.VALUES_TELEPHONE_FRANCHISE.VALUE_EXTENSION";
const heads = [
    "USER CODE",
    "GRUPO",
    "Tipo Ligação",
    "Custo Base",
    "Minuto Franquia",
    "Valor Franquia",
    "Valor Ramal",
]

export default class ShowFares extends Component {
    constructor() {
        super();
        this.state = {
            content: [],
            contentInfo: {},
            pages: 1,
            groups: null,
            page: 1,
            groupSelected: null,
            fareSelected: null,
            types: null,
        }
    }

    componentDidMount = () => {
        this.loadContent();
        this.extList();
        
    }

    loadContent = async (page = 1) => {
        // console.log('ramal', ext, 'Page', page);
        const response = await api.get(`/fares/${page}`);
        const { docs, ...contentInfo } = response.data;
        // console.log('Docs', docs);
        this.setState({ content: docs, contentInfo, pages: contentInfo.Pages.Pages, page });
        // console.log('ContentInfo', contentInfo);
    }

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

    extList = async () => {
        let groups;
        // const response = await api.get(`/groups`);
        // console.log(response);
        groups = Group.groups.map((dt) => { return { value: dt.value, label: dt.label } });

        this.setState({ groups });
        // , contentInfo, pages: contentInfo.Pages.Pages});
    }

    // List ext selected
    groupChange = async (groupSelected) => {

        this.setState({ groupSelected });
        console.log(`Group Selected: `, groupSelected);
    };

    handleSubmit = async (e) => {
        e.preventDefault();
        let types = [];
        var response;
        const { page, groupSelected } = this.state;
        try {
            response = await api.get(`/fares/${groupSelected.value}/${page}`);    
            checkArray(response.data.docs);
        } catch (err) {
            console.log(err);
            return alert('Favor escolher um grupo!');
        }
        // console.log(docs)
        const { docs, ...contentInfo } = response.data; 
        types = docs.map((tp) => { return { value: tp.TYPE_CALL_ID, label: tp.CALL_TYPE, group: tp.USER_CODE } }).filter((gp) => gp.group === groupSelected.value );
        this.setState({ content: docs, pages: contentInfo.Pages.Pages, page, types});
        this.selectDelete();
        // this.typeCall();
    }


    // typeCall = async (e) => {

    //     let types = [];
    //     const { page, groupSelected } = this.state;
    //     // const response = await api.get(`/type`);
    //     const response = await api.get(`/fares/${groupSelected.value}/${page}`);
        
    //     const { docs } = response.data;
    //     console.log(docs);
    //     types = docs.map((tp) => { return { value: tp.TYPE_CALL_ID, label: tp.CALL_TYPE, group: tp.USER_CODE } }).filter((gp) => gp.group === groupSelected.value );
    //     console.log(types);
    //     this.setState({ types })
    // }

    typeChange = typeSelected => {
        this.setState({ typeSelected });
        console.log(`Type Selected: `, typeSelected);
    }

    deleteSubmit = async (e) => {
        // /fares/delfare/2824&19
        e.preventDefault();
        const { groupSelected, typeSelected } = this.state;
        console.log('Types', typeSelected);
        await api.delete(`/fares/delfare/${groupSelected.value}&${typeSelected.value}`);
        alert(`A tarifa ${typeSelected.label} do Grupo ${groupSelected.value} foi removido com sucesso`);

        window.location.reload()
    }

    selectDelete = () => {
        const { typeSelected, types } = this.state;
        const info = (
            <div className="delete">
                <Select
                    className="selected"
                    value={typeSelected}
                    onChange={this.typeChange}
                    options={types}
                    maxMenuHeight={150}
                    placeholder="Selecione a tarifa"
                    isSearchable />
                <button className="findButton" onClick={this.deleteSubmit}>Remover Tarifa</button>
            </div>
        )

        this.setState({ info });
    }


    showFares = () => {
        const { content, page, pages } = this.state;
        // console.log('Page and pages', page, pages);
        // console.log('Content', content);
        const showFares = (
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
        return showFares;
    }


    render() {
        const { groupSelected, groups, info } = this.state;
        return (
            <div className="mainDiv">
                <div className="menu">
                    <Menu />
                </div>
                <h1>Consultar Ramais</h1>
                <div className="formShowFares">
                    <div className="finders">
                        <Select
                            className="selected"
                            value={groupSelected}
                            onChange={this.groupChange}
                            options={groups}
                            placeholder="Selecione o grupo"
                            maxMenuHeight={250}
                            isSearchable />
                        <button className="findButton" onClick={this.handleSubmit}>Pesquisar</button>
                        {info}
                    </div>

                    {this.showFares()}
                </div>
            </div>
        )
    }
}