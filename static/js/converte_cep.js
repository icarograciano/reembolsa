function formatarCEP(cep) {
    // Obtém o valor do campo CEP
    var valor = cep.value;
  
    // Remove tudo o que não é dígito
    valor = valor.replace(/\D/g, "");
  
    // Adiciona o hífen depois dos 5 primeiros dígitos
    valor = valor.replace(/(\d{5})(\d{3})/, "$1-$2");
  
    // Atualiza o valor do campo CEP
    cep.value = valor;
  }