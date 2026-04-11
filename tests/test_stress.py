import pytest
import time
import threading
import psutil
import tempfile
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
from academic_manager.builder import AcademicWork, ContentBuilder
from academic_manager.core.project_manager import ProjectManager
from academic_manager.core.pdf_generator import PDFGenerator
from academic_manager.config.settings import Config
from academic_manager.services.bing_images import process_json, download_image


@pytest.mark.slow
class TestPerformance:
    """Testes de performance e stress do sistema"""
    
    def test_pdf_generation_time_limit(self, sample_academic_metadata, sample_template_data):
        """Testa se PDF é gerado dentro do tempo limite"""
        start_time = time.time()
        
        # Simula geração de PDF com mock
        with patch('academic_manager.core.pdf_generator.AcademicWork') as mock_pdf:
            mock_instance = Mock()
            mock_pdf.return_value = mock_instance
            mock_instance.page_no.return_value = 1
            
            generator = PDFGenerator()
            result = generator.generate_pdf("test_project", sample_academic_metadata, sample_template_data)
            
        end_time = time.time()
        execution_time = end_time - start_time
        
        assert result is True
        assert execution_time < 10.0, f"PDF generation took {execution_time:.2f}s, expected < 10s"
    
    def test_large_content_processing(self):
        """Testa processamento de conteúdo muito grande"""
        # Cria conteúdo extenso
        large_text = "Lorem ipsum dolor sit amet. " * 1000  # ~27KB de texto
        
        builder = ContentBuilder()
        start_time = time.time()
        
        # Adiciona 100 parágrafos grandes
        for i in range(100):
            builder.paragraph(f"Parágrafo {i}: {large_text}")
        
        content = builder.get_content()
        end_time = time.time()
        
        assert len(content) == 100
        assert (end_time - start_time) < 1.0, "Large content processing too slow"
    
    def test_concurrent_project_creation(self):
        """Testa criação concurrent de múltiplos projetos"""
        def create_project(project_id):
            """Função para criar projeto em thread separada"""
            project_manager = ProjectManager()
            with patch('builtins.input', side_effect=[
                f'project_{project_id}', 'Engenharia', f'Aluno_{project_id}', 
                f'Título_{project_id}', 'SP', 'Disciplina', 'Prof'
            ]):
                return project_manager.create_new_project()
        
        start_time = time.time()
        
        # Cria 5 projetos concorrentemente
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(create_project, i) for i in range(5)]
            results = [future.result() for future in as_completed(futures)]
        
        end_time = time.time()
        
        # Verifica que todos foram criados
        successful_creations = [r for r in results if r is not None]
        assert len(successful_creations) == 5
        assert (end_time - start_time) < 30.0, "Concurrent project creation too slow"
    
    def test_memory_usage_large_pdf(self, sample_academic_metadata):
        """Testa uso de memória com PDF grande"""
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Cria template com muito conteúdo
        large_template = {
            "title": "Large Document Test",
            "sections": []
        }
        
        # Adiciona 50 seções com conteúdo extenso
        for i in range(50):
            section = {
                "name": f"SEÇÃO {i+1}",
                "blocks": [
                    {
                        "type": "paragraph",
                        "text": "Este é um parágrafo muito longo com bastante conteúdo para testar o uso de memória. " * 100
                    },
                    {
                        "type": "subtitle", 
                        "text": f"Subtítulo da seção {i+1}"
                    },
                    {
                        "type": "paragraph",
                        "text": "Mais conteúdo extenso para aumentar o tamanho do documento e verificar o comportamento da memória. " * 200
                    }
                ]
            }
            large_template["sections"].append(section)
        
        # Simula criação do PDF
        with patch('academic_manager.core.pdf_generator.AcademicWork') as mock_pdf:
            mock_instance = Mock()
            mock_pdf.return_value = mock_instance
            mock_instance.page_no.return_value = 50
            
            generator = PDFGenerator()
            generator.generate_pdf("large_test", sample_academic_metadata, large_template)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Verifica que o aumento de memória é razoável (< 100MB)
        assert memory_increase < 100, f"Memory usage increased by {memory_increase:.2f}MB"


@pytest.mark.slow
class TestStress:
    """Testes de stress para verificar limites do sistema"""
    
    def test_massive_image_processing(self):
        """Testa processamento de muitas imagens"""
        # Cria JSON com 20 imagens
        json_data = {
            "sections": []
        }
        
        for i in range(20):
            section = {
                "blocks": [
                    {
                        "type": "image",
                        "text": f"Test image description {i}"
                    }
                ]
            }
            json_data["sections"].append(section)
        
        with patch('academic_manager.services.bing_images.get_image_url') as mock_get_url, \
             patch('academic_manager.services.bing_images.download_image') as mock_download, \
             patch('time.sleep'):  # Remove delays
            
            mock_get_url.return_value = "https://example.com/image.jpg"
            mock_download.return_value = None
            
            start_time = time.time()
            result = process_json(json_data, "stress_test")
            end_time = time.time()
            
            # Verifica que processou todas as imagens
            assert len(result) == 20
            assert (end_time - start_time) < 60.0, "Image processing took too long"
    
    def test_extreme_content_builder_chain(self):
        """Testa method chaining extremo no ContentBuilder"""
        builder = ContentBuilder()
        start_time = time.time()
        
        # Faz chaining de 1000 operações
        for i in range(500):
            builder.paragraph(f"Para {i}").subtitle(f"Sub {i}")
        
        content = builder.get_content()
        end_time = time.time()
        
        assert len(content) == 1000  # 500 paragraphs + 500 subtitles
        assert (end_time - start_time) < 5.0, "Extreme chaining too slow"
    
    def test_rapid_project_operations(self, temp_workspace):
        """Testa operações rápidas e repetitivas em projetos"""
        project_manager = ProjectManager()
        operations_count = 100
        
        start_time = time.time()
        
        for i in range(operations_count):
            # Simula operações rápidas
            projects = project_manager._get_next_project_number()
            assert isinstance(projects, int)
            
            # Simula listagem de projetos
            from academic_manager.core.file_manager import FileManager
            FileManager.list_projects()
        
        end_time = time.time()
        avg_time_per_operation = (end_time - start_time) / operations_count
        
        assert avg_time_per_operation < 0.01, f"Average operation time {avg_time_per_operation:.4f}s too slow"


@pytest.mark.slow 
class TestResourceLimits:
    """Testes para verificar comportamento em condições de recursos limitados"""
    
    def test_disk_space_simulation(self, temp_workspace):
        """Simula comportamento com pouco espaço em disco"""
        # Este teste simula erro de espaço em disco
        with patch('builtins.open', side_effect=OSError("No space left on device")):
            project_manager = ProjectManager()
            
            with patch('builtins.input', side_effect=['test_project', 'Curso', 'Aluno', 'Titulo', 'Local', 'Disc', 'Prof']):
                result = project_manager.create_new_project()
                
            assert result is None, "Should handle disk space error gracefully"
    
    def test_network_timeout_simulation(self):
        """Simula timeouts de rede"""
        import requests
        
        with patch('academic_manager.services.aistudio_chat.requests.post', 
                   side_effect=requests.exceptions.Timeout("Request timeout")):
            
            from academic_manager.services.aistudio_chat import get_template_json
            result = get_template_json("Test assignment", False, "test_project")
            
            assert result is None, "Should handle network timeout gracefully"
    
    def test_corrupted_file_handling(self, temp_workspace):
        """Testa comportamento com arquivos corrompidos"""
        # Cria arquivo JSON corrompido
        project_path = temp_workspace / "corrupted_project"
        Path(project_path).mkdir(parents=True, exist_ok=True)
        
        corrupted_json = Path(project_path) / "settings.json"
        with open(corrupted_json, "w") as f:
            f.write('{"invalid": json syntax}')  # JSON inválido
        
        project_manager = ProjectManager()
        result = project_manager.update_existing_project()
        
        # Deve tratar graciosamente JSON corrompido
        assert result is None


@pytest.mark.integration
class TestEndToEndPerformance:
    """Testes end-to-end focados em performance"""
    
    def test_complete_workflow_performance(self, temp_workspace, sample_assignment_content):
        """Testa performance do workflow completo"""
        # Setup mocks
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = {
            "candidates": [{
                "content": {
                    "parts": [{
                        "text": json.dumps({
                            "title": "Teste Performance",
                            "sections": [
                                {
                                    "name": "INTRODUÇÃO",
                                    "blocks": [
                                        {"type": "paragraph", "text": "Introdução do teste"},
                                        {"type": "image", "text": "Test image", "position": "center"}
                                    ]
                                }
                            ]
                        })
                    }]
                }
            }]
        }

        with patch('academic_manager.services.aistudio_chat.requests.post', return_value=mock_api_response), \
             patch('academic_manager.services.bing_images.get_image_url', return_value="https://example.com/image.jpg"), \
             patch('academic_manager.services.bing_images.download_image', return_value=None):
            
            import time
            start_time = time.time()
            
            # 1. Criar projeto
            mock_inputs = ['perf_test', 'Assignment text', 'FIM'] + ['Value'] * 50
            with patch('builtins.input', side_effect=mock_inputs):
                (Config.BASE_DIR / "perf_test").mkdir(parents=True, exist_ok=True)
                (Config.BASE_DIR / "assignments").mkdir(parents=True, exist_ok=True)
                project_manager = ProjectManager()
                project_result = project_manager.create_new_project()
            
            assert project_result is not None
            
            # 2. Gerar template
            from academic_manager.core.template_generator import TemplateGenerator
            (Config.BASE_DIR / "perf_test").mkdir(parents=True, exist_ok=True) # Ensure it exists for prompt.md
            template_path = Path(temp_workspace) / "test_template.json"
            template_result = TemplateGenerator.generate_ai_template(
                sample_assignment_content, {}, template_path, "perf_test"
            )
            
            assert template_result is not None
            
            # 3. Gerar PDF
            with patch('academic_manager.core.pdf_generator.AcademicWork'):
                generator = PDFGenerator()
                pdf_result = generator.generate_pdf("perf_test", project_result[1], template_result)
            
            assert pdf_result is True
            
            end_time = time.time()
            total_time = end_time - start_time
            
            assert total_time < 15.0, f"Complete workflow took {total_time:.2f}s, expected < 15s"


class TestMemoryLeaks:
    """Testes para detectar vazamentos de memória"""
    
    def test_repeated_content_builder_usage(self):
        """Testa uso repetido do ContentBuilder sem vazamentos"""
        initial_memory = psutil.Process().memory_info().rss
        
        # Usa ContentBuilder 100 vezes
        for i in range(100):
            builder = ContentBuilder()
            
            # Adiciona conteúdo
            for j in range(10):
                builder.paragraph(f"Paragraph {j} in iteration {i}")
                builder.subtitle(f"Subtitle {j} in iteration {i}")
            
            # Limpa conteúdo
            builder.clear()
            del builder
        
        final_memory = psutil.Process().memory_info().rss
        memory_growth = (final_memory - initial_memory) / 1024 / 1024  # MB
        
        # Permite crescimento mínimo, mas não vazamentos significativos
        assert memory_growth < 10, f"Possible memory leak: {memory_growth:.2f}MB growth"
    
    def test_academic_work_memory_cleanup(self, sample_academic_metadata):
        """Testa limpeza de memória no AcademicWork"""
        initial_memory = psutil.Process().memory_info().rss
        
        # Cria e destrói múltiplas instâncias
        for i in range(50):
            academic_work = AcademicWork(sample_academic_metadata, "test_logo.png")
            
            # Adiciona conteúdo
            academic_work.add_section("Test Section", "Test content")
            
            # Força limpeza
            del academic_work
        
        final_memory = psutil.Process().memory_info().rss
        memory_growth = (final_memory - initial_memory) / 1024 / 1024  # MB
        
        assert memory_growth < 20, f"Possible memory leak in AcademicWork: {memory_growth:.2f}MB growth"


@pytest.mark.slow
class TestConcurrency:
    """Testes de concorrência e thread safety"""
    
    def test_thread_safe_file_operations(self, temp_workspace):
        """Testa operações de arquivo thread-safe"""
        from academic_manager.core.file_manager import FileManager
        
        def file_operation(thread_id):
            """Operação de arquivo em thread separada"""
            try:
                FileManager.ensure_directories_exist()
                projects = FileManager.list_projects()
                assignments = FileManager.list_assignments()
                return len(projects) + len(assignments)
            except Exception as e:
                return f"Error in thread {thread_id}: {e}"
        
        # Executa operações concorrentes
        results = []
        threads = []
        
        for i in range(10):
            thread = threading.Thread(target=lambda: results.append(file_operation(i)))
            threads.append(thread)
            thread.start()
        
        # Espera todos terminarem
        for thread in threads:
            thread.join()
        
        # Verifica que não houve erros
        errors = [r for r in results if isinstance(r, str) and "Error" in r]
        assert len(errors) == 0, f"Thread safety issues: {errors}"
    
    def test_concurrent_pdf_generation(self, sample_academic_metadata):
        """Testa geração concurrent de PDFs"""
        def generate_pdf(pdf_id):
            """Gera PDF em thread separada"""
            template = {
                "title": f"PDF {pdf_id}",
                "sections": [
                    {
                        "name": "TEST",
                        "blocks": [{"type": "paragraph", "text": f"Content {pdf_id}"}]
                    }
                ]
            }
            
            with patch('academic_manager.core.pdf_generator.AcademicWork'):
                generator = PDFGenerator()
                return generator.generate_pdf(f"project_{pdf_id}", sample_academic_metadata, template)
        
        start_time = time.time()
        
        # Gera 5 PDFs concorrentemente
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(generate_pdf, i) for i in range(5)]
            results = [future.result() for future in as_completed(futures)]
        
        end_time = time.time()
        
        # Verifica que todos foram gerados
        assert all(results), "Some PDFs failed to generate"
        assert (end_time - start_time) < 20.0, "Concurrent PDF generation too slow"


@pytest.mark.api
class TestAPIPerformance:
    """Testes de performance para chamadas de API"""
    
    @staticmethod
    def test_api_response_time():
        """Testa tempo de resposta da API"""
        import time
        # Simula resposta lenta
        def slow_response(*args, **kwargs):
            time.sleep(0.1)  # Simula latência
            response = Mock()
            response.status_code = 200
            response.json.return_value = {
                "candidates": [{
                    "content": {
                        "parts": [{"text": '{"title": "Test"}'}]
                    }
                }]
            }
            return response
        
        with patch('academic_manager.services.aistudio_chat.requests.post', side_effect=slow_response):
            (Config.BASE_DIR / "test_project").mkdir(parents=True, exist_ok=True)
            from academic_manager.services.aistudio_chat import get_template_json
            
            start_time = time.time()
            result = get_template_json("Test assignment", False, "test_project")
            end_time = time.time()
        
        assert result is not None
        assert (end_time - start_time) < 2.0, "API call took too long"
    
    @staticmethod
    def test_api_timeout_handling():
        """Testa tratamento de timeout em APIs"""
        import requests
        import time
        
        with patch('academic_manager.services.aistudio_chat.requests.post',
                   side_effect=requests.exceptions.Timeout):
            (Config.BASE_DIR / "test").mkdir(parents=True, exist_ok=True)
            from academic_manager.services.aistudio_chat import get_template_json
            
            start_time = time.time()
            result = get_template_json("Test", False, "test")
            end_time = time.time()
            
            assert result is None
            assert (end_time - start_time) < 1.0, "Timeout handling too slow"


# Utilities para benchmarking
class PerformanceBenchmark:
    """Classe utilitária para benchmarking"""
    
    def __init__(self, test_name: str):
        self.test_name = test_name
        self.start_time = None
        self.end_time = None
        self.memory_start = None
        self.memory_end = None
    
    def __enter__(self):
        self.start_time = time.time()
        self.memory_start = psutil.Process().memory_info().rss
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        self.memory_end = psutil.Process().memory_info().rss
        
        execution_time = self.end_time - self.start_time
        memory_diff = (self.memory_end - self.memory_start) / 1024 / 1024  # MB
        
        print(f"\n=== BENCHMARK: {self.test_name} ===")
        print(f"Execution time: {execution_time:.3f}s")
        print(f"Memory usage: {memory_diff:.2f}MB")
        print("=" * (len(self.test_name) + 20))


# Exemplo de uso do benchmark
def test_benchmark_example():
    """Exemplo de como usar o benchmark"""
    with PerformanceBenchmark("Content Builder Performance"):
        builder = ContentBuilder()
        
        for i in range(100):
            builder.paragraph(f"Test paragraph {i}")
            builder.subtitle(f"Test subtitle {i}")
        
        content = builder.get_content()
        assert len(content) == 200


if __name__ == "__main__":
    # Executa apenas testes de performance
    pytest.main([
        __file__,
        "-v",
        "-m", "slow or integration",
        "--tb=short"
    ])