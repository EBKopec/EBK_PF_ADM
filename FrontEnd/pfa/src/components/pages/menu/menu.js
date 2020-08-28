import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Dropdown, Menu } from 'semantic-ui-react';
import { logout } from "../../services/auth";
import "./styles.css";

const styleLink = document.createElement("link");
styleLink.rel = "stylesheet";
styleLink.href = "https://cdn.jsdelivr.net/npm/semantic-ui/dist/semantic.min.css";
document.head.appendChild(styleLink);

export default class MainMenu extends Component {
  state = {
    result: null
  }

  handleItemClick = async (e, name) => {
    this.setState({ activeItem: name });
  }

  handleLogout() {

    logout();

  }


  render() {
    const { activeItem } = this.state
    return (
      <div className="mainMenu">
        <Menu inverted
          vertical
          fixed="left"
          size="huge"
          color="orange">
          <Dropdown.Item>
            Portal de Faturamento - Adm
        </Dropdown.Item>

          {/* Menu Faturamento */}
          <Dropdown item text='Faturamento'>
            <Dropdown.Menu>

              <Dropdown.Item
                icon='edit'
                name='billing'
                text='Faturar'
                as={Link} to='/app/faturamento'
                active={activeItem === 'billing'}
                onClick={this.handleItemClick}>
                {/* <Link className="link" to="/app/faturamento"> */}
                {/* <Header size="small"><Icon name='edit' />Faturar</Header> */}
                {/* </Link> */}
              </Dropdown.Item>

              <Dropdown.Item
                icon='file alternate'
                name='showBilling'
                text='Visualizar Faturamento'
                as={Link} to='/app/fechamentos'
                active={activeItem === 'showBilling'}
                onClick={this.handleItemClick}>
              </Dropdown.Item>

              <Dropdown.Item
                icon='percent'
                text='Consumo Total'
                name='consumeTotal'
                as={Link} to='/app/consumoTotal'
                active={activeItem === 'consumeTotal'}
                onClick={this.handleItemClick}>
              </Dropdown.Item>
            </Dropdown.Menu>
          </Dropdown>

          {/* Menu Backup Faturamento */}
          <Dropdown item text='Backup Faturamento'>
            <Dropdown.Menu>
              {/* <Dropdown.Item
                icon='save'
                text='Realizar Backup'
                name='backup'
                as={Link} to='/app/backup'
                active={activeItem === 'backup'}
                onClick={this.handleItemClick}>
              </Dropdown.Item> */}

              <Dropdown.Item
                icon='save'
                name='checkBilling'
                text='Consultar Backups'
                as={Link} to='/app/backups'
                active={activeItem === 'checkBilling'}
                onClick={this.handleItemClick}>
              </Dropdown.Item>
              {/* 
              <Dropdown.Item
                icon='save outline'
                text='Backups à Realizar'
                name='toBackup'
                as={Link} to='/app/toBackup'
                active={activeItem === 'toBackup'}
                onClick={this.handleItemClick}>
              </Dropdown.Item> */}

            </Dropdown.Menu>
          </Dropdown>

          {/* Menu Manter Ramais */}
          <Dropdown item text='Manter Ramais'>
            <Dropdown.Menu>

              <Dropdown.Item
                icon='phone square'
                text='Registrar Ramais'
                name='extReg'
                as={Link} to='/app/ramais'
                active={activeItem === 'extReg'}
                onClick={this.handleItemClick}>
              </Dropdown.Item>

              <Dropdown.Item
                icon='phone'
                text='Manter Ramais'
                name='extActivate'
                as={Link} to='/app/manterRamais'
                active={activeItem === 'extActivate'}
                onClick={this.handleItemClick}>
              </Dropdown.Item>

              {/* <Dropdown.Item
                icon='phone'
                text='Mudar Ramal de Grupo'
                name='extChangeGroup'
                as={Link} to="/app/mudarRamaisGrupo"
                active={activeItem === 'extChangeGroup'}
                onClick={this.handleItemClick}>
              </Dropdown.Item>

              <Dropdown.Item
                icon='phone'
                text='Desativar Ramais'
                name='extDeactivate'
                as={Link} to='/app/desativarRamais'
                active={activeItem === 'extDeactivate'}
                onClick={this.handleItemClick}>
              </Dropdown.Item> */}
            </Dropdown.Menu>
          </Dropdown>

          {/* Menu Consultar Ramais */}
          <Dropdown item text='Consultar Ramais'>
            <Dropdown.Menu>

              <Dropdown.Item
                icon='phone square'
                text='Listar Ramais'
                name='extensions'
                as={Link} to='/app/listar'
                active={activeItem === 'extensions'}
                onClick={this.handleItemClick}>
              </Dropdown.Item>
{/* 
              <Dropdown.Item
                icon='phone'
                text='Ramal'
                name='ext'
                as={Link} to='/app/listarRamal'
                active={activeItem === 'ext'}
                onClick={this.handleItemClick}>
              </Dropdown.Item> */}

              <Dropdown.Item
                icon='phone'
                text='Ramais Mês'
                name='extMonth'
                as={Link} to='/app/listarRamaisMes'
                active={activeItem === 'extMonth'}
                onClick={this.handleItemClick}>
              </Dropdown.Item>

              <Dropdown.Item
                icon='phone'
                text='Ramais Quantidade'
                name='extQty'
                as={Link} to='/app/listarRamaisQtde'
                active={activeItem === 'extQty'}
                onClick={this.handleItemClick}>
              </Dropdown.Item>

            </Dropdown.Menu>
          </Dropdown>

          {/* Menu Tipo de Ligações */}
          <Dropdown item text='Manter Tipo de Ligações'>
            <Dropdown.Menu>

              <Dropdown.Item
                icon='teletype'
                text='Manter'
                name='typeReg'
                as={Link} to='/app/tipoLigacoes'
                active={activeItem === 'typeReg'}
                onClick={this.handleItemClick}>
              </Dropdown.Item>

              {/* <Dropdown.Item
                icon='teletype'
                text='Listar'
                name='type'
                as={Link} to='/app/showTipoLigacoes'
                active={activeItem === 'type'}
                onClick={this.handleItemClick}>
              </Dropdown.Item>

              <Dropdown.Item
                icon='delete'
                text='Remover'
                name='typeDel'
                as={Link} to='/app/removerTipoLigacoes'
                active={activeItem === 'typeDel'}
                onClick={this.handleItemClick}>
              </Dropdown.Item> */}
            </Dropdown.Menu>
          </Dropdown>

          {/* Menu Tarifas */}
          <Dropdown item text='Manter Tarifas'>
            <Dropdown.Menu>

              <Dropdown.Item
                icon='teletype'
                text='Registrar Tarifas'
                name='typeReg'
                as={Link} to='/app/tarifas'
                active={activeItem === 'typeReg'}
                onClick={this.handleItemClick}>
              </Dropdown.Item>

              <Dropdown.Item
                icon='teletype'
                text='Listar Tarifas'
                name='fareShow'
                as={Link} to='/app/listarTarifas'
                active={activeItem === 'fareShow'}
                onClick={this.handleItemClick}>
              </Dropdown.Item>

              {/* <Dropdown.Item
                icon='teletype'
                text='Atualizar Tarifas'
                name='fareUpdt'
                as={Link} to='/app/atualizarTarifas'
                active={activeItem === 'fareUpdt'}
                onClick={this.handleItemClick}>
              </Dropdown.Item>

              <Dropdown.Item
                icon='delete'
                text='Remover Tarifas'
                name='fareDel'
                as={Link} to='/app/removerTarifas'
                active={activeItem === 'fareDel'}
                onClick={this.handleItemClick}>
              </Dropdown.Item> */}

            </Dropdown.Menu>
          </Dropdown>


          <Dropdown.Item
            icon='sign out'
            text='Logout'
            name='logout'
            as={Link} to='/'
            active={activeItem === 'logout'}
            onClick={this.handleLogout}>
            {/* <Icon name='sign out' /> */}
          </Dropdown.Item>
        </Menu>
      </div>
    )
  }
}