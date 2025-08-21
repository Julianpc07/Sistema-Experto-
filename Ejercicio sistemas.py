import os
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class Rule:
    """Clase para representar una regla del sistema experto"""
    conditions: Dict[str, Any]
    diagnosis: str
    description: str
    recommendations: List[str]
    severity: str = "medium"  # low, medium, high, critical

class CarDiagnosticExpert:
    """Sistema Experto para Diagnóstico Automotriz"""
    
    def __init__(self):
        self.knowledge_base = self._initialize_knowledge_base()
        self.questions = self._initialize_questions()
        self.user_answers = {}
        self.current_step = 0
        
    def _initialize_knowledge_base(self) -> Dict[str, Rule]:
        """Inicializa la base de conocimiento con las reglas"""
        return {
            'rule1': Rule(
                conditions={'starts': False, 'dash_lights': False},
                diagnosis="Batería descargada",
                description="Las luces del tablero apagadas junto con la imposibilidad de arrancar indican que la batería no tiene carga suficiente.",
                recommendations=[
                    "Verificar voltaje de la batería con multímetro (debe ser ~12.6V)",
                    "Intentar arrancar con cables puente",
                    "Revisar terminales de batería (corrosión/sulfatación)",
                    "Considerar reemplazar la batería si tiene más de 3-4 años",
                    "Verificar el alternador si la batería se descarga frecuentemente"
                ],
                severity="medium"
            ),
            
            'rule2': Rule(
                conditions={'starts': False, 'dash_lights': True},
                diagnosis="Fallo en el motor de arranque",
                description="Si las luces funcionan pero el motor no arranca, el problema está en el sistema de arranque.",
                recommendations=[
                    "Verificar si se escucha el 'click' del solenoide",
                    "Revisar fusibles del sistema de arranque",
                    "Comprobar conexiones del motor de arranque",
                    "Verificar el interruptor de encendido",
                    "Puede requerir reemplazo del motor de arranque"
                ],
                severity="high"
            ),
            
            'rule3': Rule(
                conditions={'starts': True, 'stalls_when_accelerating': True},
                diagnosis="Problema en el suministro de combustible",
                description="El motor arranca pero no puede mantener la potencia, sugiere falta de combustible o presión inadecuada.",
                recommendations=[
                    "Verificar nivel de combustible en el tanque",
                    "Revisar y reemplazar filtro de combustible",
                    "Comprobar presión de la bomba de combustible",
                    "Limpiar inyectores de combustible",
                    "Verificar calidad del combustible"
                ],
                severity="medium"
            ),
            
            'rule4': Rule(
                conditions={'black_smoke': True},
                diagnosis="Mezcla rica de combustible",
                description="El humo negro indica combustión incompleta por exceso de combustible en la mezcla aire-combustible.",
                recommendations=[
                    "Revisar y limpiar/reemplazar filtro de aire",
                    "Verificar sensores de oxígeno (lambda)",
                    "Comprobar inyectores (pueden estar goteando)",
                    "Revisar sistema de gestión del motor (ECU)",
                    "Verificar sensor de flujo de aire (MAF)"
                ],
                severity="medium"
            ),
            
            'rule5': Rule(
                conditions={'white_smoke': True},
                diagnosis="Falla en la junta de culata",
                description="Humo blanco constante indica que el refrigerante está entrando a la cámara de combustión.",
                recommendations=[
                    "PARAR EL MOTOR INMEDIATAMENTE",
                    "Verificar nivel de refrigerante",
                    "Revisar si hay aceite con aspecto lechoso",
                    "Comprobar temperatura del motor",
                    "Realizar prueba de compresion",
                    "Consultar mecanico especializado URGENTE"
                ],
                severity="critical"
            )
        }
    
    def _initialize_questions(self) -> List[Dict]:
        """Inicializa las preguntas del sistema"""
        return [
            {
                'id': 'starts',
                'question': '¿El automóvil arranca?',
                'type': 'boolean'
            },
            {
                'id': 'dash_lights',
                'question': '¿Las luces del tablero se encienden al girar la llave?',
                'type': 'boolean',
                'condition': lambda answers: answers.get('starts') == False
            },
            {
                'id': 'stalls_when_accelerating',
                'question': '¿El motor se apaga cuando aceleras?',
                'type': 'boolean',
                'condition': lambda answers: answers.get('starts') == True
            },
            {
                'id': 'black_smoke',
                'question': '¿Sale humo negro por el escape?',
                'type': 'boolean'
            },
            {
                'id': 'white_smoke',
                'question': '¿Sale humo blanco constante por el escape?',
                'type': 'boolean'
            }
        ]
    
    def clear_screen(self):
        """Limpia la pantalla"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Imprime el encabezado del sistema"""
        print("=" * 60)
        print("SISTEMA EXPERTO PARA DIAGNOSTICO AUTOMOTRIZ")
        print("=" * 60)
        print("Diagnostico inteligente de fallas en vehiculos")
        print("-" * 60)
    
    def print_progress(self, current: int, total: int):
        """Imprime la barra de progreso"""
        percentage = (current / total) * 100 if total > 0 else 0
        filled = int(percentage / 5)  # 20 caracteres máximo
        bar = "█" * filled + "░" * (20 - filled)
        print(f"\nProgreso: [{bar}] {percentage:.0f}% ({current}/{total})")
    
    def get_applicable_questions(self) -> List[Dict]:
        """Obtiene las preguntas aplicables según las respuestas actuales"""
        applicable = []
        for question in self.questions:
            if 'condition' not in question:
                applicable.append(question)
            elif question['condition'](self.user_answers):
                applicable.append(question)
        return applicable
    
    def ask_question(self, question: Dict) -> bool:
        """Hace una pregunta al usuario y retorna la respuesta"""
        while True:
            print(f"\n{question['question']}")
            print("\n1. Si")
            print("2. No")
            
            try:
                choice = input("\nSeleccione una opcion (1 o 2): ").strip()
                
                if choice == '1':
                    return True
                elif choice == '2':
                    return False
                else:
                    print("Por favor, ingrese 1 para Si o 2 para No")
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n\nDiagnostico cancelado por el usuario.")
                return False
    
    def find_diagnosis(self) -> Optional[Rule]:
        """Encuentra el diagnóstico basado en las respuestas del usuario"""
        for rule_name, rule in self.knowledge_base.items():
            matches = True
            
            # Verificar si todas las condiciones de la regla se cumplen
            for condition, expected_value in rule.conditions.items():
                if self.user_answers.get(condition) != expected_value:
                    matches = False
                    break
            
            if matches:
                return rule
        
        return None
    
    def print_symptoms_summary(self):
        """Imprime un resumen de los síntomas identificados"""
        positive_symptoms = []
        
        for question in self.questions:
            question_id = question['id']
            if self.user_answers.get(question_id) == True:
                symptom = question['question'].replace('¿', '').replace('?', '')
                positive_symptoms.append(symptom)
        
        if positive_symptoms:
            print("\nSINTOMAS IDENTIFICADOS:")
            print("-" * 40)
            for i, symptom in enumerate(positive_symptoms, 1):
                print(f"  {i}. {symptom}")
    
    def print_diagnosis(self, diagnosis: Rule):
        """Imprime el diagnóstico y las recomendaciones"""
        severity_levels = {
            'low': 'BAJA',
            'medium': 'MEDIA',
            'high': 'ALTA',
            'critical': 'CRITICA'
        }
        
        print(f"\nDIAGNOSTICO ENCONTRADO")
        print("=" * 50)
        print(f"Posible causa: {diagnosis.diagnosis}")
        print(f"Severidad: {severity_levels.get(diagnosis.severity, 'MEDIA')}")
        print(f"\nDescripcion:")
        print(f"   {diagnosis.description}")
        
        print(f"\nRECOMENDACIONES:")
        print("-" * 30)
        for i, recommendation in enumerate(diagnosis.recommendations, 1):
            print(f"  {i}. {recommendation}")
        
        # Advertencia especial para casos críticos
        if diagnosis.severity == 'critical':
            print("\n" + "!" * 50)
            print("   ATENCION: Esta es una falla CRITICA")
            print("   Consulte un mecanico especializado INMEDIATAMENTE")
            print("!" * 50)
    
    def print_no_diagnosis(self):
        """Imprime mensaje cuando no se puede determinar un diagnóstico"""
        print("\nDIAGNOSTICO NO DETERMINADO")
        print("=" * 40)
        print("No se pudo identificar una causa especifica")
        print("con los sintomas proporcionados.")
        print("\nRecomendaciones generales:")
        print("  1. Consultar con un mecanico especializado")
        print("  2. Realizar una revision mas detallada")
        print("  3. Verificar codigos de error con scanner OBD")
    
    def run_diagnosis(self):
        """Ejecuta el proceso completo de diagnóstico"""
        self.clear_screen()
        self.print_header()
        
        print("\nBienvenido al sistema de diagnostico automotriz")
        print("Responderemos algunas preguntas para ayudarte a identificar el problema.")
        
        input("\nPresione Enter para comenzar...")
        
        # Obtener preguntas aplicables
        applicable_questions = self.get_applicable_questions()
        total_questions = len(applicable_questions)
        
        # Hacer preguntas
        for i, question in enumerate(applicable_questions):
            self.clear_screen()
            self.print_header()
            self.print_progress(i, total_questions)
            
            print(f"\nPregunta {i + 1} de {total_questions}")
            
            answer = self.ask_question(question)
            self.user_answers[question['id']] = answer
            
            # Actualizar preguntas aplicables si es necesario
            if question['id'] in ['starts']:
                applicable_questions = self.get_applicable_questions()
                # Filtrar preguntas ya respondidas
                applicable_questions = [q for q in applicable_questions 
                                     if q['id'] not in self.user_answers]
        
        # Mostrar resultados
        self.clear_screen()
        self.print_header()
        self.print_progress(total_questions, total_questions)
        
        self.print_symptoms_summary()
        
        diagnosis = self.find_diagnosis()
        
        if diagnosis:
            self.print_diagnosis(diagnosis)
        else:
            self.print_no_diagnosis()
    
    def run(self):
        """Función principal del sistema"""
        while True:
            try:
                self.user_answers = {}
                self.current_step = 0
                
                self.run_diagnosis()
                
                print("\n" + "=" * 60)
                restart = input("\nDesea realizar otro diagnostico? (s/n): ").lower().strip()
                
                if restart not in ['s', 'si', 'y', 'yes']:
                    print("\nGracias por usar el sistema de diagnostico automotriz!")
                    break
                    
            except KeyboardInterrupt:
                print("\n\nSistema finalizado por el usuario.")
                break
            except Exception as e:
                print(f"\nError inesperado: {e}")
                input("\nPresione Enter para continuar...")

def main():
    """Función principal"""
    print("Iniciando Sistema Experto de Diagnóstico Automotriz...")
    time.sleep(1)
    
    expert_system = CarDiagnosticExpert()
    expert_system.run()

if __name__ == "__main__":
    main()