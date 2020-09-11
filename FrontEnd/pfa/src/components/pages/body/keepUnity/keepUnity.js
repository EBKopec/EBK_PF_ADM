/* eslint-disable jsx-a11y/anchor-is-valid */
import React, { Component } from "react";
import { withRouter } from "react-router-dom";
import Menu from "../../menu/menu";
import { Form, Container } from "./styles";
import Select from 'react-select';
import api from "../../../services/api";


class keepUnity extends Component {
    constructor(props) {
        super(props);
        this.state = {
            local: null,
            setor: null,
            localSelected: null,
            setorSelected: null,
            locals: [],
            setores: [],
        };
    }
    componentDidMount = () => {
        // console.log("Data", this.state.data);
        this.unity();
        // this.pendentGroup();
    }


    localChange = localSelected => {
        // const { user_group_id, ...data } = this.state;
        // console.log('Estado ', data.linha);
        this.setState({ localSelected });
        console.log(`Local Selected: `, localSelected );
    };

    setorChange = setorSelected => {
        this.setState({setorSelected});
        console.log(`Setor Selected: `, setorSelected );
    }

    unity = async (e) => {
        let locals = [];
        let setores = [];

        const local = await api.get(`/local`);
        const setor = await api.get(`/setor`);
        // console.log(local);
        locals = local.data.map((id_local) => { return { value: id_local.id_local, label: id_local.descricao_local } });
        setores = setor.data.map((id_setor) => { return { value: id_setor.id_setor, label: id_setor.descricao_setor }})
        // console.log("Years", ano);
        this.setState({ locals: locals, setores: setores });
    }

    handleSubmitAssoc = async (e) => {
        e.preventDefault();
        const { localSelected, setorSelected } = this.state;
        if ( !localSelected || !setorSelected ){
            alert("Favor associar o Local ao Setor!");
        } else {
            let id_local = localSelected.value;
            let id_setor = setorSelected.value;
            try {
                console.log(id_local, id_setor)
                await api.post("/setplace", {id_local, id_setor});
                alert(`Unidade ${localSelected.label} - ${setorSelected.label} associado com sucesso!`);
                window.location.reload(); 
            } catch (err){
                console.log(err);
                alert(`Ocorreu um erro ao associar ${localSelected.label} com ${setorSelected.label}`);
            }
        }


    }

    handleSubmit = async (e) => {
        e.preventDefault();
        const { local, setor } = this.state;
        // console.log(`Validacao ${linha}, ${user_group_id.value}, ${tipo_linha}, ${data_envio_nova}, ${status}`)
        if (!local) {
            alert("Favor Preencher o Local!");
        } else {
            try {
                // let dest_setor = setor === null  ? 'Sem Setor' : setor;
                // const post = 
                await api.post("/setlocal", { descricao_local:local});
                if (setor !== null){
                    await api.post("/setsetor", { descricao_setor:setor});
                }

                // const { data } = post;
                alert(`Unidade ${local} - ${setor} cadastrado com sucesso!`);
                // this.setState({local:null, setor:null});
                window.location.reload(); 

            } catch (err) {
                console.log(err);
                alert("Ocorreu um erro ao registrar o local");
            }
        }
    }


    render() {
        const { locals, localSelected, setores, setorSelected } = this.state;
        // console.log("Info", info, groupSelected);

        return (
            <div className="mainDiv">
                <div className="menu">
                    <Menu />
                </div>
                <p>Manter Unidades</p>
                <div className="formExt">
                    <Container>

                        <Form onSubmit={this.handleSubmit}>
                            <a>Local</a>
                            <input
                                type="text"
                                placeholder="Local"
                                onChange={e => this.setState({ local: e.target.value })}
                                required
                            />
                            <a>Setor</a>
                            <input
                                type="text"
                                placeholder="Setor"
                                onChange={e => this.setState({ setor: e.target.value })}
                            />
                            <button type="submit">Cadastrar</button>
                        </Form>
                        <Form onSubmit={this.handleSubmitAssoc}>
                        <a>Local</a>
                        <Select
                                className="selected"
                                value={localSelected}
                                onChange={this.localChange}
                                options={locals}
                                maxMenuHeight={150}
                                placeholder="Selecione o Local"
                                isSearchable 
                                required
                                />
                        <a>Setor</a>
                        <Select
                                className="selected"
                                value={setorSelected}
                                onChange={this.setorChange}
                                options={setores}
                                maxMenuHeight={150}
                                placeholder="Selecione o Setor"
                                isSearchable 
                                required
                                />
                            <button type="submit">Criar Unidade</button>
                        </Form>
                        
                    </Container>
                </div>
            </div>

        )
    }
}

export default withRouter(keepUnity);