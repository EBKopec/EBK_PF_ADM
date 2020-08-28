import styled from "styled-components";

export const Container = styled.div`
    display: flex;
    align-itens: center;
    justify-content: center;
    height: 100%;
`;

export const Form = styled.form`
  width: 500px;
  background: #fff;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: justify;
  img {
    width: 200px;
    margin: 10px 0 40px;
  }
  p {
    color: #ff3333;
    margin-bottom: 15px;
    border: 1px solid #ff3333;
    padding: 10px;
    width: 100%;
    text-align: center;
  }
input{
    flex: 1;
    margin-bottom: 5px;
    padding: 10px 20px;
    color: #777;
    font-size: 15px;
    width: 100%;
    border: 1px solid #ddd;
    &::placeholder {
      color: #999;
    }
  }

input.dtActivate {
    flex: none;
    height: 45px;
   }

  button {
    color: #fff;
    font-size: 16px;
    background: #ff9b42;
    height: 45px;
    border: 0;
    border-radius: 5px;
    width: 100%;
    cursor: pointer;
  }
  hr {
    margin: 20px 0;
    border: none;
    border-bottom: 1px solid #cdcdcd;
    width: 100%;
  }
  a {
    text-align: left;
    font-size: 18px;
    font-weight: bold;
    color: #999;
    text-decoration: none;
    margin-top: 10px;
    margin-bottom: 5px;

  }
  .selected {
    width: 100%;
    font-weight: bold;
    padding: 5px;
  }
`;