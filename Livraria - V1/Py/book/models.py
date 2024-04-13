from django.db import models

class Bairro(models.Model):
    bairro_id = models.AutoField(primary_key=True)
    bairro = models.CharField(max_length=100)

    def __str__(self):
        return self.bairro


class Cep(models.Model):
    cep_id = models.AutoField(primary_key=True)
    cep = models.CharField(max_length=10)

    def __str__(self):
        return self.cep


class Endereco(models.Model):
    endereco_id = models.AutoField(primary_key=True)
    endereco = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class Cidade(models.Model):
    cidade_id = models.AutoField(primary_key=True)
    cidade = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Estado(models.Model):
    estado_id = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Livro(models.Model):
    livro_id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    editora = models.CharField(max_length=100)
    genero = models.CharField(max_length=50)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.TextField(max_length=5000)
    descricao = models.TextField(max_length=5000)

    def __str__(self):
        return self.titulo


class Cliente(models.Model):
    cliente_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    numero = models.IntegerField()
    complemento = models.CharField(max_length=200)
    bairro = models.ForeignKey(Bairro, on_delete=models.CASCADE)
    cep = models.ForeignKey(Cep, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20)
    celular = models.CharField(max_length=20)
    email = models.EmailField()
    senha = models.CharField(max_length=100)
    como_soube = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class Venda(models.Model):
    venda_id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_venda = models.DateField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venda {self.venda_id} - Cliente: {self.cliente.nome}"


class ItemVenda(models.Model):
    itemvenda_id = models.AutoField(primary_key=True)
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()

    def __str__(self):
        return f"Item {self.itemvenda_id} - Livro: {self.livro.titulo}, Quantidade: {self.quantidade}"
