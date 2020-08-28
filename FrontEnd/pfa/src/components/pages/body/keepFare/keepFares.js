/* eslint-disable jsx-a11y/anchor-is-valid */
import React, { Component } from "react";
import { withRouter } from "react-router-dom";
import Menu from "../../menu/menu";
import { Form, Container } from "./styles";
import Select from 'react-select';
import api from "../../../services/api";
import Groups from "../../../utils/groups.json";


class keepFares extends Component {
    constructor() {
        super();
        this.state = {
            linha: null,
            user_group_id: null,
            tipo_linha: null,
            data_envio_nova: null,
            data_alteracao: null,
            status: null,
            groups: null,
            group: null,
            typeSelected: null,
            groupSelected: null,
            types: null,
            data: null,
        };
    }
    componentDidMount = () => {
        // console.log("Data", this.state.data);
        this.pendentGroup();
        this.typeCall();
    }

    handleSubmit = async (e) => {
        e.preventDefault();
        const { groupSelected, typeSelected, CUSTO, DATA_ALTERACAO, FRANQUIA_MIN, FRANQUIA_VALOR, VALOR_RAMAL, BATCH_ID } = this.state;
        // console.log(`Validacao ${linha}, ${user_group_id.value}, ${tipo_linha}, ${data_envio_nova}, ${status}`)
        if (!groupSelected || !typeSelected || !CUSTO || !DATA_ALTERACAO || !FRANQUIA_MIN || !FRANQUIA_VALOR || !VALOR_RAMAL || !BATCH_ID ) {
            alert("Preencha todos os dados!");
        } else {
            let USER_ID = groupSelected.value;
            let TIPO_ID = typeSelected.value;
            try {
                // const post = 
                await api.post("/fares/regfare", { USER_ID, TIPO_ID, CUSTO, DATA_ALTERACAO, FRANQUIA_MIN, FRANQUIA_VALOR, VALOR_RAMAL, BATCH_ID });
                // const { data } = post;
                alert('Tarifa Cadastrada com Sucesso!');
                this.props.history.push("/app/tarifas");
                window.location.reload()
                // this.setState( state => ({info: [ data, ...state.info ]}));

            } catch (err) {
                console.log(err);
                alert("Ocorreu um erro ao registrar o ramal");
            }
        }
    }

    groupChange = groupSelected => {
        // const { user_group_id, ...data } = this.state;
        // console.log('Estado ', data.linha);
        this.setState({ groupSelected });
        console.log(`Group Selected: `, groupSelected);
    };

    pendentGroup = () => {
        let groups = [];
        groups = Groups.groups.map((dt) => { return { value: dt.value, label: dt.label } })
        this.setState({ groups: groups })
    }

    typeChange = typeSelected => {
        this.setState({typeSelected});
        console.log(`Type Selected: `, typeSelected);
    }

    typeCall = async () => {
        let types = [];
        const response = await api.get(`/type`);
        const { data } = response;
        types = data.map((tp) => {return {value:tp.ID, label: tp.TIPO}});
        this.setState({types})
    }


    render() {
        const { groups, groupSelected, typeSelected, types } = this.state;
        // console.log("Info", info, groupSelected);

        return (
            <div className="mainDiv">
                <div className="menu">
                    <Menu />
                </div>
                <p>Manter Tarifas</p>
                <div className="formFares">
                    <Container>

                        <Form onSubmit={this.handleSubmit}>
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
                            <a>Tipo Tarifa</a>
                            <Select
                                className="selected"
                                value={typeSelected}
                                onChange={this.typeChange}
                                options={types}
                                maxMenuHeight={150}
                                placeholder="Selecione o Tipo de ligação"
                                isSearchable
                                required
                            />
                            <a>Custo</a>
                            <input
                                type="number"
                                placeholder="Custo"
                                onChange={e => this.setState({ CUSTO: e.target.value })}
                                required
                            />
                            <a>Data Alteração</a>
                            <input
                                type="date"
                                placeholder="DATA ALTERACAO"
                                onChange={e => this.setState({ DATA_ALTERACAO: e.target.value })}
                                required
                            />
                            <a>Franquia Minutos</a>
                            <input
                                type="number"
                                placeholder="Franquia Minutos"
                                onChange={e => this.setState({ FRANQUIA_MIN: e.target.value })}
                                required
                            />
                            <a>Franquia Valor</a>
                            <input
                                type="number"
                                placeholder="Franquia Valor"
                                onChange={e => this.setState({ FRANQUIA_VALOR: e.target.value })}
                                required
                            />
                            <a>Valor Ramal</a>
                            <input
                                type="number"
                                min="0.01" step="0.01" max="2500"
                                placeholder="Valor Ramal"
                                onChange={e => this.setState({ VALOR_RAMAL: e.target.value })}
                                required
                            />
                            <a>Batch</a>
                            <input
                                type="number"
                                placeholder="Batch"
                                onChange={e => this.setState({ BATCH_ID: e.target.value })}
                                required
                            />
                            <button type="submit">Registrar</button>
                        </Form>
                    </Container>
                </div>
            </div>

        )
    }
}

export default withRouter(keepFares);