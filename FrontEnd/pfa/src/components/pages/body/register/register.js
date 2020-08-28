import React, { Component } from "react";
import { Link, withRouter } from "react-router-dom";

import Logo from "../../../images/nova_logo.png";

import { Form, Container } from "./styles";
import api from "../../../services/api";

class Register extends Component {
    state = {
        username : "",
        email : "",
        password : ""
    };

    handleRegister = async e => {
        e.preventDefault();
        const { username, email, password } = this.state;
        if ( !username || !email || !password ){
            alert("Preencha todos os dados para se cadastrar!");
        } else {
            try {
                await api.post("/users/register", { username, email, password });
                this.props.history.push("/");
            } catch (err) {
                console.log(err);
                alert("Ocorreu um erro ao registrar sua conta");
            }
        }
    };

    render(){
        return (
            <Container>
                <Form onSubmit={this.handleRegister}>
                    <img src={Logo} alt="Nova Fibra logo"/>
                    {this.state.error && <p>{this.state.error}</p>}
                    <input 
                        type="text"
                        placeholder="Nome do Usuário"
                        onChange={e => this.setState({ username: e.target.value })}
                        required
                    />
                    <input
                        type="email"
                        placeholder="Endereço de E-mail"
                        onChange={e => this.setState({ email: e.target.value })}
                        required
                    />
                    <input
                        type="password"
                        placeholder="Senha"
                        onChange={e => this.setState({ password: e.target.value })}
                        required
                    />
                    <button type="submit">Registrar Usuário</button>
                    <hr/>
                    <Link to="/">Fazer Login</Link>
                </Form>
            </Container>
        );
    }
}

export default withRouter(Register);