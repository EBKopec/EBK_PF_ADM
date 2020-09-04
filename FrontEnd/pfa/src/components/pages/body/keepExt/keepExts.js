/* eslint-disable jsx-a11y/anchor-is-valid */
import React, { Component } from "react";
import Menu from "../../menu/menu";
import Select from 'react-select';
import api from "../../../services/api";
import Groups from "../../../utils/groups.json";
import { Form, Container } from "./styles";

export default class registerExts extends Component {
    constructor() {
        super();
        this.state = {
            page_num: 1,
            extSelected: null,
            extGroupSelected: null,
            selectedOption: null,
            ext: null,
            group: null,
            info: [],
            status: ['P','N'],
            dt_event: null,
            toChange: 'Y',
        }
    }

    componentDidMount = () => {
        this.pendentExt(this.state.status);
        this.pendentGroup();

    }

    // list all exts per status
    pendentExt = async (status) => {
        // const { page_num } = this.state;
        let exts = [];
        const response = await api.get(`/extKeep/${status}`);
        const { data } = response;
        exts = data.map((dt) => { return { value: dt.linha, label: dt.linha } })
        this.setState({ info: data, ext: exts });
    }

    // select groups from json to fill list of groups
    pendentGroup = () => {
        let groups = [];
        groups = Groups.groups.map((dt) => { return { value: dt.value, label: dt.label } })
        this.setState({ group: groups })
    }

    // List ext selected
    extChange = async (extSelected) => {
        const { status } = this.state;
        let selectedGroup;
        const response = await api.get(`/extKeep/${status}`);
        const { data } = response;
        selectedGroup = data.map((dt) => { return { value: dt.user_group_id, label: dt.Grupo, ext: dt.linha } }).find((sg) => sg.ext === extSelected.value)
        this.setState({ extSelected, extGroupSelected: selectedGroup });
    };

    // select group
    extGroupChange = extGroupSelected => {
        this.setState({ extGroupSelected });
        console.log(`Grupo Selected: `, extGroupSelected);
    }

    // handle action on radio button
    handleOptionChange = async changeEvent => {
        let status = null;
        let event = null;
        let toChange = null;

        if (changeEvent.target.id === 'activateExt') {
            status = ['P','N'];
            toChange = 'Y';
            event = changeEvent.target.value;
        }
        if (changeEvent.target.id === 'changeExt') {
            status = 'Y';
            event = changeEvent.target.value;
        }
        if (changeEvent.target.id === 'deactivateExt') {
            status = 'Y';
            toChange = 'N'
            event = changeEvent.target.value;
        }

        this.setState({ selectedOption: event, status, toChange });
        this.pendentExt(status);
    }

    handleSubmit = async (e) => {
        e.preventDefault();
        const { extSelected, extGroupSelected, toChange, dt_event, selectedOption } = this.state;
        // const group = extGroupSelected.value;
        // console.log("Result", selectedOption);
        
        //Activate ext
        if (selectedOption === 'activate' ) {
            if (!extSelected || !dt_event || !toChange) {
                alert("Preencha todos os dados!");
            } else {
                const ext = extSelected.value;
                const status = toChange;
                const data_validacao_cliente = dt_event;
                try {
                    // const post = 
                    await api.post(`/extensions/updtext/${ext}`, { status, data_validacao_cliente });
                    alert(`Ramal ${extSelected.value} atualizado com sucesso!`);
                } catch (err) {
                    console.log(err);
                    alert(`Ocorreu um erro ao ativar ${extSelected.value} o ramal`);
                }
            }
        } 
        // Change Group
        if (selectedOption === 'changeExt' ){
            if (!extSelected || !dt_event || !extGroupSelected ){
                alert("Preencha todos os dados!");
            }else{
                const ext = extSelected.value;
                const user_group_id = extGroupSelected.value;
                const data_alteracao = dt_event; 
                try {
                    // const post = 
                    await api.post(`/extensions/updtext/${ext}`, { user_group_id, data_alteracao });
                    alert(`Ramal ${extSelected.value} atualizado com sucesso!`);
                } catch (err) {
                    console.log(err);
                    alert(`Ocorreu um erro ao trocar o ramal ${extSelected.value} de grupo`);
                }
            }
        }
        
        // Deactivate ext
        if (selectedOption === 'deactivateExt' ){
            if (!extSelected || !toChange || !dt_event ){
                alert("Preencha todos os dados!");
            }else{
                const ext = extSelected.value;
                const status = toChange;
                const data_cancelamento = dt_event; 
                try {
                    // const post = 
                    await api.post(`/extensions/updtext/${ext}`, { status, data_cancelamento });
                    alert(`Ramal ${extSelected.value} desconectado!`);
                } catch (err) {
                    console.log(err);
                    alert(`Ocorreu um erro ao desativar o ramal ${extSelected.value}`);
                }
            }
        }

        
        window.location.reload();
    }

    render() {
        const { extSelected, ext, extGroupSelected, group, selectedOption } = this.state;
        return (
            <div className="mainDiv">
                <div className="menu">
                    <Menu />
                </div>

                <div className="formKeepExt">
                    <p>Manter Ramais</p>
                    <Container>
                        <Form onSubmit={this.handleSubmit}>
                            <Select
                                className="selected"
                                value={extSelected}
                                onChange={this.extChange}
                                options={ext}
                                maxMenuHeight={150}
                                placeholder="Selecione o Ramal"
                                isSearchable />
                            <Select
                                className="selected"
                                value={extGroupSelected}
                                onChange={this.extGroupChange}
                                options={group}
                                maxMenuHeight={150}
                                placeholder="Selecione o Grupo"
                                isSearchable />

                            <div className="radio">
                                <input
                                    id="activateExt"
                                    type="radio"
                                    className="radio"
                                    name="radioActive"
                                    value="activate"
                                    checked={selectedOption === "activate"}
                                    onChange={this.handleOptionChange} />
                                <label for="activateExt">Ativar Ramal</label>
                                <input
                                    id="changeExt"
                                    name="radioChange"
                                    className="radio"
                                    type="radio"
                                    value="changeExt"
                                    checked={selectedOption === "changeExt"}
                                    onChange={this.handleOptionChange} />
                                <label for="changeExt"> Mudar Ramal de Grupo</label>
                                <input
                                    id="deactivateExt"
                                    type="radio"
                                    className="radio"
                                    name="radioDeactivate"
                                    value="deactivateExt"
                                    checked={selectedOption === "deactivateExt"}
                                    onChange={this.handleOptionChange} />
                                <label for="deactivateExt">Desconectar</label>
                            </div>
                            <a>Data de ativação / alteração ou desconexão</a>
                            <input className="dtActivate"
                                type="date"
                                placeholder="Data de Ativação"
                                onChange={e => this.setState({ dt_event: e.target.value })}
                                required
                            />
                            <button type="submit">Executar</button>
                        </Form>
                    </Container>
                </div>
            </div >

        )
    }
}