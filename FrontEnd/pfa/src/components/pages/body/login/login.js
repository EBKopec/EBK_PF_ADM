import React, { Component } from "react";
import { Link, withRouter } from "react-router-dom";
import Logo from "../../../images/nova_logo.png";
import api from "../../../services/api";
import { login, clear } from "../../../services/auth";

import { Form, Container } from "./styles";

class Login extends Component{
    state = {
        username: "",
        password: ""
    };


    handleLogin = async e => {
        e.preventDefault();
        const { username, password } = this.state;
        if ( !username || !password ) {
            alert("Preencha Usuário e Senha!");
        } else {
            try {
                const response = await api.post("/login", { username, password });
                clear(response.data.token);
                login(response.data.token);
                this.props.history.push("/app");
            } catch (err){
                alert("Houve um problema, verifique se seus dados de acesso estão corretos!");
            }
        }
    };

    render(){
        return (
            <Container>
                <Form onSubmit={this.handleLogin}>
                    <img src={Logo} alt="Nova Fibra logo"/>
                    {this.state.error && <p>{this.state.error}</p>}
                    <input
                      type="username"
                      autoComplete="username"
                      placeholder="Usuário"
                      onChange={e => this.setState({ username: e.target.value })}
                      required
                    />
                    <input
                      type="password"
                      autoComplete="password"
                      placeholder="Password"
                      onChange={e => this.setState({ password: e.target.value })}
                      required
                    />
                    <button type="submit">Login</button>
                    <hr/>
                    <Link to="/users/register">Registrar Usuário</Link>
                </Form>
            </Container>
        );
    }
}
export default withRouter(Login);