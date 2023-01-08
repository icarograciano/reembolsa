function verificarCnpj(cnpj) {
    // Remover qualquer caractere que não seja um dígito
    cnpj = cnpj.replace(/\D/g, '');
  
    // Verificar se o CNPJ possui 14 dígitos
    if (cnpj.length !== 14) {
      document.getElementById('cnpj-error').innerHTML = 'CNPJ inválido';
      return false;
    }
  
    // Calcular o primeiro dígito verificador
    let soma = 0;
    let resto;
    let multiplicadores = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2];
    for (let i = 0; i < 12; i++) {
      soma += parseInt(cnpj[i]) * multiplicadores[i];
    }
    resto = soma % 11;
    if (resto < 2) {
      resto = 0;
    } else {
      resto = 11 - resto;
    }
    if (resto !== parseInt(cnpj[12])) {
      document.getElementById('cnpj-error').innerHTML = 'CNPJ inválido';
      return false;
    }
  
    // Calcular o segundo dígito verificador
    soma = 0;
    multiplicadores = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2];
    for (let i = 0; i < 13; i++) {
      soma += parseInt(cnpj[i]) * multiplicadores[i];
    }
    resto = soma % 11;
    if (resto < 2) {
      resto = 0;
    } else {
      resto = 11 - resto;
    }
    if (resto !== parseInt(cnpj[13])) {
      document.getElementById('cnpj-error').innerHTML = 'CNPJ inválido';
      return false;
    }
  
    // Se chegou até aqui, o CNPJ é válido
    document.getElementById('cnpj-error').innerHTML = '';
    return true;
  }
  
  
  

  document.getElementById('cnpj').addEventListener('blur', function(e) {
    verificarCnpj(e.target.value);
  });
  