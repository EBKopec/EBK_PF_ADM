import React, { Component } from "react";
import Menu from "../../menu/menu";
import Select from 'react-select';
import Table from '../../../utils/table/table';
import api from "../../../services/api";
import { checkArray } from '../../../utils/bytes';

const columns = "linha.Grupo.tipo_linha.status.data_envio_nova.data_validacao_cliente.data_alteracao.data_cancelamento.descricao_local.descricao_setor";
const heads = [ 
    "LINHA",
    "GRUPO",
    "TIPO LINHA",
    "STATUS",
    "DATA DE CADASTRO",
    "DATA ATIVAÇÃO",
    "DATA ALTERAÇÃO",
    "DATA CANCELAMENTO",
    "LOCAL",
    "SETOR"
]


export default class SearchExts extends Component {
    constructor(){
        super();
        this.state={
            content: [],
            contentInfo: {},
            pages: 1,
            ext:0,
            exts: 0,
            page:1
        }
    }

    componentDidMount = () => {
        this.loadContent();
        this.extList();
    }

    loadContent = async (page = 1) => {
        const { ext } = this.state;
        // console.log('ramal', ext, 'Page', page);
        const response = await api.get(`/extensions/${ext}/${page}`);
        const { docs, ...contentInfo } = response.data;
        console.log('Docs', docs);
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
        let exts;
        const response = await api.get(`/extKeep/A`);
        // console.log(response);
        const { data } = response;
        exts = data.map((dt) => { return { value: dt.linha, label: dt.linha } });
        
        this.setState({ exts });
            // , contentInfo, pages: contentInfo.Pages.Pages});
    }

    // List ext selected
    extChange = async (extSelected) => {
        this.setState({ extSelected });
        console.log(`Ext Selected: `, extSelected);
    };

    handleSubmit = async (e) => {
        e.preventDefault();
        const { page, extSelected } = this.state;
        try {
            checkArray(extSelected.value);
        } catch (error) {
            return alert('Favor escolher um ramal para pesquisa!');
        }
        const response = await api.get(`/extensions/${extSelected.value}/${page}`);
        const { docs, ...contentInfo } = response.data;
       
        this.setState({content: docs, pages: contentInfo.Pages.Pages, page, extSelected: null})

    }

    showExts = () => {
        const { content, page, pages } = this.state;
        // console.log('Page and pages', page, pages);
        // console.log('Content', content);
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


    render() {
        const { extSelected, exts } = this.state;
        return (
            <div className="mainDiv">
                <div className="menu">
                    <Menu />
                </div>
                <h1>Consultar Ramais</h1>
                <div className="finders">
                    <Select
                        className="selected"
                        value={extSelected}
                        onChange={this.extChange}
                        options={exts}
                        placeholder="Selecione o Ramal"
                        maxMenuHeight={250}
                        isSearchable/>
                    <button className="findButton" onClick={this.handleSubmit}>Pesquisar</button>
                </div>

                {this.showExts()}
            </div>
        )
    }
}