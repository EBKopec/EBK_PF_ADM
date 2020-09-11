/* eslint-disable jsx-a11y/anchor-is-valid */
import React, { Component } from "react";
import { withRouter } from "react-router-dom";
import Menu from "../../menu/menu";
import { Form, Container } from "./styles";
import Select from 'react-select';
import api from "../../../services/api";
import Groups from "../../../utils/groups.json";

// const groups = [
//     { value: 2824, label: "Prefeitura de Ponta Grossa - PMPG" },
//     { value: 2831, label: "Prefeitura de Ponta Grossa - SME - ESCOLA" },
//     { value: 2832, label: "Prefeitura de Ponta Grossa - SME - CMEI" },
//     { value: 2833, label: "Prefeitura de Ponta Grossa - SMS - PAB" },
//     { value: 2834, label: "Prefeitura de Ponta Grossa - SMS - FAE" },
//     { value: 2835, label: "Prefeitura de Ponta Grossa - SMS - AIH" },
//     { value: 2855, label: "Prefeitura de Ponta Grossa - SAMU" },
//     { value: 2857, label: "Prefeitura de Ponta Grossa - BOMBEIROS" }
// ]

class KeepExts extends Component {
    constructor(){
        super();
        this.state ={
            linha: null,
            user_group_id: null,
            tipo_linha: null,
            data_envio_nova: null,
            data_alteracao: null,
            status: null,
            groups: null,
            group: null,
            groupSelected: null,
            localSelected: null,
            info: [],
            data: null,
        };
    }
    componentDidMount = () => {
        // console.log("Data", this.state.data);
        this.history();
        this.pendentGroup();
        this.local();
    }

    handleSubmit = async (e) => {
        e.preventDefault();
        const { linha, groupSelected, localSelected, tipo_linha, data_envio_nova, data_alteracao, status} = this.state;
        // console.log(`Validacao ${linha}, ${user_group_id.value}, ${tipo_linha}, ${data_envio_nova}, ${status}`)
        if ( !linha || !groupSelected || !tipo_linha || !data_envio_nova || !data_alteracao || !status || !localSelected){
            alert("Preencha todos os dados!");
        } else {
            let user_group_id = groupSelected.value;
            let id_local_setor = localSelected.value;
            try {
                // const post = 
                await api.post("/extensions/regext", {linha, user_group_id, tipo_linha, data_envio_nova, data_alteracao, status, id_local_setor});
                // const { data } = post;
                alert('Ramal Cadastrado com Sucesso!');
                this.props.history.push("/app/ramais");
                this.history();
                // this.setState( state => ({info: [ data, ...state.info ]}));
                
            } catch (err) {
                console.log(err);
                alert("Ocorreu um erro ao registrar o ramal");
            }
        }
    }

    history = async (e) => {
        const response = await api.get(`/extKeep/P`);
        const {data} = response;
        // console.log('History', data);
        this.setState({info: data});
    }

    groupChange = groupSelected => {
        // const { user_group_id, ...data } = this.state;
        // console.log('Estado ', data.linha);
        this.setState({ groupSelected });
        console.log(`Group Selected: `, groupSelected );
    };

    localChange = localSelected => {
        this.setState({localSelected});
        console.log(`Local Selected: `, localSelected );
    }

    pendentGroup = () => {
        let groups = [];
        groups = Groups.groups.map((dt) => { return { value: dt.value, label: dt.label } })
        this.setState({ groups: groups })
    }

    local = async (e) => {
        let locals = [];

        const local = await api.get(`/localsetor`);
        // console.log(local);
        locals = local.data.map((id_local) => { return { value: id_local.id_local_setor, label: id_local.Local_Setor } });
        // console.log("Years", ano);
        this.setState({ locals: locals });
    }


    render(){
        const { groups, groupSelected, locals, localSelected, info } = this.state;
        // console.log("Info", info, groupSelected);
        
        return (
            <div className="mainDiv">
                <div className="menu">
                    <Menu />
                </div>
                <p>Cadastrar Ramais</p>
                <div className="formExt">
                    <Container>
                        
                        <Form onSubmit={this.handleSubmit}>
                        <a>Ramal ou Linha</a>
                        <input 
                            type="number"
                            placeholder="Ramal ou Linha"
                            onChange={ e => this.setState({ linha: e.target.value })}
                            required
                            />
                        <a>Grupos</a>
                        <Select
                                className="selected"
                                value={groupSelected}
                                onChange={this.groupChange}
                                options={groups}
                                maxMenuHeight={150}
                                placeholder="Selecione o Grupo"
                                isSearchable 
                                required
                                />
                        <a>Unidade</a>
                        <Select
                                className="selected"
                                value={localSelected}
                                onChange={this.localChange}
                                options={locals}
                                maxMenuHeight={150}
                                placeholder="Selecione a Unidade"
                                isSearchable 
                                required
                                />
                        <a>Tipo de Linha</a>
                        <input 
                            type="text"
                            placeholder="Tipo de Linha"
                            onChange={ e => this.setState({ tipo_linha: e.target.value })}
                            required
                            />
                        <a>Data de Cadastro</a>
                        <input 
                            type="date"
                            placeholder="Data de Cadastro"
                            onChange={ e => this.setState({ data_envio_nova: e.target.value })}
                            required
                            />
                        <a>Data de Alteração</a>
                        <input 
                            type="date"
                            placeholder="Data de Alteração"
                            onChange={ e => this.setState({ data_alteracao: e.target.value })}
                            required
                        />
                        <a>Status</a>
                        <input 
                            type="text"
                            placeholder="Status"
                            pattern="[a-zA-Z]"
                            title="Números não são aceitos!"
                            maxlength="1"
                            onChange={ e => this.setState({ status: e.target.value })}
                            required
                            />
                        <button type="submit">Registrar</button>
                        </Form>
                        
                        <div className="groups">
                            <div className="table">
                                <table>
                                    <thead>
                                        <tr>
                                            <th>Ramal</th>
                                            <th>Grupo</th>
                                            <th>Tipo de Linha</th>
                                            <th>Data de Cadastro</th>
                                            <th>Status</th>
                                        </tr>
                                    </thead>
                                    {info.map(data => (
                                    <tbody key={data.linha}>
                                        <tr>
                                            <td>{data.linha}</td>
                                            <td>{data.Grupo}</td>
                                            <td>{data.tipo_linha}</td>
                                            <td>{data.data_envio_nova}</td>
                                            <td>{data.status}</td>
                                        </tr>
                                    </tbody>
                                    ))}
                                </table>

                            </div>
                            
                        </div>
                        </Container>
                </div>
            </div>

        )
    }
}

export default withRouter(KeepExts);