/* eslint-disable jsx-a11y/anchor-is-valid */
import React, { Component } from "react";
import { withRouter } from "react-router-dom";
import Menu from "../../menu/menu";
import { Form, Container } from "./styles";
import api from "../../../services/api";
import Checkbox from "../../../utils/checkBox";


class keepCallTypes extends Component {
    constructor(props) {
        super(props);
        this.state = {
            TIPO_DESC: null,
            DATA_ALTERACAO: null,
            info: [],
            item: [],
            checkedItems: new Map(),
        };
        this.handleCheckboxChange = this.handleCheckboxChange.bind(this);
    }
    componentDidMount = () => {
        // console.log("Data", this.state.data);
        this.history();
        // this.pendentGroup();
    }

    handleSubmit = async (e) => {
        e.preventDefault();
        const { TIPO_DESC, DATA_ALTERACAO } = this.state;
        // console.log(`Validacao ${linha}, ${user_group_id.value}, ${tipo_linha}, ${data_envio_nova}, ${status}`)
        if (!TIPO_DESC || !DATA_ALTERACAO) {
            alert("Preencha todos os dados!");
        } else {
            try {
                // const post = 
                await api.post("/type", { TIPO_DESC, DATA_ALTERACAO });
                // const { data } = post;
                alert('Tipo de Ligação cadastrada com Sucesso!');
                this.props.history.push("/app/tipoLigacoes");
                this.history();
                // this.setState( state => ({info: [ data, ...state.info ]}));

            } catch (err) {
                console.log(err);
                alert("Ocorreu um erro ao registrar o ramal");
            }
        }
    }

    history = async (e) => {
        const response = await api.get(`/type`);
        const { data } = response;
        // console.log('History', data);
        this.setState({ info: data });
    }

    deleteType = async () => {
        const { checkedItems } = this.state;
        for (const [key] of checkedItems) {
            // console.log(`Teste ${key}: ${value}`);
            await api.delete(`/type/${key}`);
        }
        this.setState(prevState => ({ checkedItems: prevState.checkedItems.set(null) }));
        this.history();
    }


    handleCheckboxChange(e) {
        const item = e.target.name;
        const isChecked = e.target.checked;
        this.setState(prevState => ({ checkedItems: prevState.checkedItems.set(item, isChecked) }));
        console.log("item, isChecked", item, isChecked);
    }

    render() {
        const { info } = this.state;
        // console.log("Info", info, groupSelected);

        return (
            <div className="mainDiv">
                <div className="menu">
                    <Menu />
                </div>
                <p>Manter Tipo de Ligações</p>
                <div className="formExt">
                    <Container>

                        <Form onSubmit={this.handleSubmit}>
                            <a>Tipo de Ligação</a>
                            <input
                                type="text"
                                placeholder="Tipo de Ligação"
                                onChange={e => this.setState({ TIPO_DESC: e.target.value })}
                                required
                            />
                            <a>Data de Cadastro</a>
                            <input
                                type="date"
                                placeholder="Data de Cadastro"
                                onChange={e => this.setState({ DATA_ALTERACAO: e.target.value })}
                                required
                            />
                            <button type="submit">Cadastrar</button>
                        </Form>

                        <div className="groups">
                            <div className="table">
                                <table>
                                    <thead>
                                        <tr>
                                            <th>ID</th>
                                            <th>TIPO</th>
                                            <th>DATA DE CADASTRO</th>
                                            <th>REMOVER</th>
                                        </tr>
                                    </thead>

                                    <tbody>
                                        {info.map(data => (
                                            <tr key={data.ID}>
                                                <td>{data.ID}</td>
                                                <td>{data.TIPO}</td>
                                                <td>{data.DATA_ALTERACAO}</td>
                                                <td><Checkbox
                                                    className="check"
                                                    name={data.ID}
                                                    checked={this.state.checkedItems.get(data.ID)}
                                                    onChange={this.handleCheckboxChange} />
                                                    <label>Remover</label>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                                <div className="finders">
                                    <button className="findButton" onClick={this.deleteType}>Remover</button>
                                </div>
                            </div>

                        </div>
                    </Container>
                </div>
            </div>

        )
    }
}

export default withRouter(keepCallTypes);