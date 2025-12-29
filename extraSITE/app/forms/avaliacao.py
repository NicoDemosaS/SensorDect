from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField, RadioField
from wtforms.validators import DataRequired, NumberRange, Optional, Length


class AvaliacaoForm(FlaskForm):
    """Formulário de avaliação."""
    
    nota = RadioField(
        'Avaliação Geral',
        choices=[('5', '⭐⭐⭐⭐⭐ Excelente'), 
                 ('4', '⭐⭐⭐⭐ Muito Bom'), 
                 ('3', '⭐⭐⭐ Bom'), 
                 ('2', '⭐⭐ Regular'), 
                 ('1', '⭐ Ruim')],
        validators=[DataRequired(message='Selecione uma nota')],
        coerce=int
    )
    
    pontualidade = RadioField(
        'Pontualidade',
        choices=[('5', '5'), ('4', '4'), ('3', '3'), ('2', '2'), ('1', '1')],
        validators=[Optional()],
        coerce=int
    )
    
    profissionalismo = RadioField(
        'Profissionalismo',
        choices=[('5', '5'), ('4', '4'), ('3', '3'), ('2', '2'), ('1', '1')],
        validators=[Optional()],
        coerce=int
    )
    
    comunicacao = RadioField(
        'Comunicação',
        choices=[('5', '5'), ('4', '4'), ('3', '3'), ('2', '2'), ('1', '1')],
        validators=[Optional()],
        coerce=int
    )
    
    comentario = TextAreaField(
        'Comentário (opcional)',
        validators=[Optional(), Length(max=500, message='Comentário muito longo (máx 500 caracteres)')]
    )
