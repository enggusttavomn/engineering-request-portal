"""
Testes unitários da app de portal.

Este arquivo contém testes para:
- Modelos de Solicitação, Log e Dispositivo
- Views de dashboards e funcionalidades
- Fluxo de aprovação e status
- Validações de negócio

Para executar os testes:
    python manage.py test portal

Para executar com verbosidade:
    python manage.py test portal -v 2
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch

from .models import Solicitacao, SolicitacaoLog, SolicitacaoStatus


class WorkflowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("solicitante")
        self.solicitacao = Solicitacao.objects.create(titulo="Demonstracao", criado_por=self.user)

    def test_approval_records_actor_and_audit_log(self):
        old_status = self.solicitacao.status
        self.solicitacao.mudar_status(SolicitacaoStatus.APROVADO, self.user, "Aprovado no teste")
        self.solicitacao.refresh_from_db()
        self.assertEqual(self.solicitacao.status, SolicitacaoStatus.APROVADO)
        self.assertEqual(self.solicitacao.aprovado_por, self.user)
        self.assertIsNotNone(self.solicitacao.aprovado_em)
        log = self.solicitacao.logs.get()
        self.assertEqual((log.status_de, log.status_para), (old_status, SolicitacaoStatus.APROVADO))
        self.assertEqual(log.alterado_por, self.user)

    def test_repeated_status_does_not_duplicate_audit_log(self):
        self.solicitacao.mudar_status(self.solicitacao.status, self.user)
        self.assertFalse(self.solicitacao.logs.exists())

    def test_status_is_rolled_back_when_audit_write_fails(self):
        old_status = self.solicitacao.status
        with patch.object(SolicitacaoLog.objects, "create", side_effect=RuntimeError("audit unavailable")):
            with self.assertRaises(RuntimeError):
                self.solicitacao.mudar_status(SolicitacaoStatus.APROVADO, self.user)
        self.solicitacao.refresh_from_db()
        self.assertEqual(self.solicitacao.status, old_status)
        self.assertIsNone(self.solicitacao.aprovado_em)

    def test_unknown_status_is_rejected(self):
        with self.assertRaises(ValueError):
            self.solicitacao.mudar_status("UNKNOWN", self.user)
        self.assertFalse(self.solicitacao.logs.exists())


