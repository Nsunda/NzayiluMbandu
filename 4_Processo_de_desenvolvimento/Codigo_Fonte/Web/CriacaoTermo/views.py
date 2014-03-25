from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from CriacaoTermo.models import Estado, Certificacao, Kik, Port

class IndexView(generic.ListView):
    template_name = 'CriacaoTermo/index.html'
    context_object_name = 'latest_port_list'

    def get_queryset(self):
        """Retorna os últimos vinte termopt publicados"""
        return Port.objects.filter(
            data_pubpt_lte=timezone.now()
        ).order_by('-data_pubpt')[:20]


class DetailView(generic.DetailView):
    model = Port
    template_name = 'CriacaoTermo/detail.html'
    def get_queryset(self):
        """
        Excluir qualquer Termopt que não foi publicado.
        """
        return Port.objects.filter(data_pubpt__lte=timezone.now())
        

class ResultsView(generic.DetailView):
    model = Port
    template_name = 'CriacaoTermo/results.html'

    def termokk(request, port_id):
    p = get_object_or_404(Port, pk=port_id)
    try:
        created_kik = p.kik_set.get(pk=request.POST['kik'])
    except (KeyError, Kik.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'CriacaoTermo/detail.html', {
            'kik': p,
            'error_message': "Termo em kikongo não inserido.",
        })
    else:
        seld_termopt.termokk += 1
        selected_termopt.conceitokk += 1
        selected_termokk.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('CriacaoTermo:results', args=(p.id,)))


class TermoptIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_termopt(self):
        """
        The detail view of a Termopt with a pub_date in the future should
        return a 404 not found.
        """
        future_termopt = create_termopt(termopt='Future termopt.', days=5)
        response = self.client.get(reverse('CriacaoTermo:detail', args=(future_termopt.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_termopt(self):
        """
        The detail view of a poll with a pub_date in the past should display
        the poll's question.
        """
        past_termopt = create_termpt(question='Past Termopt.', days=-5)
        response = self.client.get(reverse('CriacaoTermo:detail', args=(past_termopt.id,)))
        self.assertContains(response, past_termopt.termopt, status_code=200)

''' PARA O TERMO KIKONGO'''
class IndexView(generic.ListView):
    template_name = 'CriacaoTermo/index.html'
    context_object_name = 'latest_termokkcriado_list'

    def get_queryset(self):
        """Retorna os últimos vinte termokk publicados"""
        return Termokk.objects.filter(
            data_pubkk_lte=timezone.now()
        ).order_by('-data_pubkk')[:20]

class DetailView(generic.DetailView):
    model = Termokk
    template_name = 'CriacaoTermo/detail.html'
    def get_queryset(self):
        """
        Excluir qualquer Termokk que não foi publicado.
        """
        return Termokk.objects.filter(data_pubkk__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Termokk
    template_name = 'CriacaoTermo/results.html'

    def certificado(request, termokk_id):
    p = get_object_or_404(Termokk, pk=termokk_id)
    try:
        selected_certificacao = p.certificacao_set.get(pk=request.POST['certificado'])
        selected_certificacao = p.certificacao_set.get(pk=request.POST['observacao'])
    except (KeyError, Termokk.DoesNotExist):
        # Redisplay the termokk cerfificação form.
        return render(request, 'CriacaoTermo/detail.html', {
            'Termokk': p,
            'error_message': "Termo em Certificado não inserido.",
        })
    else:
        selected_certificacao.certificado += 1
        selected_certificacao.observacao += 1
        selected_certificacao.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('CriacaoTermo:results', args=(p.id,)))


class TermokkIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_termokk(self):
        """
        The detail view of a Termokk with a pub_date in the future should
        return a 404 not found.
        """
        future_termokk = create_termokk(termokk='Future termokk.', days=5)
        response = self.client.get(reverse('CriacaoTermo:detail', args=(future_termokk.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_termokk(self):
        """
        The detail view of a termokk with a pub_date in the past should display
        the termokk do Termokk.
        """
        past_termokk = create_termkk(termokk='Past Termokk.', days=-5)
        response = self.client.get(reverse('CriacaoTermo:detail', args=(past_termokk.id,)))
        self.assertContains(response, past_termokk.termokk, status_code=800)


'''PARA A CERTIFICAÇÃO '''

class IndexView(generic.ListView):
    template_name = 'CriacaoTermo/index.html'
    context_object_name = 'latest_cerfiticacaocriado_list'

    def get_queryset(self):
        """Retorna os últimos vinte certificações publicados"""
        return Certificacao.objects.filter(
            data_cert_lte=timezone.now()
        ).order_by('-data_cert')[:20]

class DetailView(generic.DetailView):
    model = Certificacao
    template_name = 'CriacaoTermo/detail.html'
    def get_queryset(self):
        """
        Excluir qualquer certificação que não foi publicado.
        """
        return Certificacao.objects.filter(data_cert__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Certificacao
    template_name = 'CriacaoTermo/results.html'

    def estado(request, certificacao_id):
    p = get_object_or_404(Termokk, pk=termokk_id)
    try:
        selected_estado = p.estado_set.get(pk=request.POST['estado'])
    except (KeyError, Estado.DoesNotExist):
        # Redisplay the termokk cerfificação form.
        return render(request, 'CriacaoTermo/detail.html', {
            'certificacao': p,
            'error_message': "Certificado em Estado não inserido.",
        })
    else:
        selected_estado.estado_texto += 1
        selected_estado.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('CriacaoTermo:results', args=(p.id,)))


class CertificacaoIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_certificacao(self):
        """
        The detail view of a certificacao with a pub_date in the future should
        return a 404 not found.
        """
        future_certififcacao = create_certificacao(estado_texto='Future estado.', days=5)
        response = self.client.get(reverse('CriacaoTermo:detail', args=(future_estado.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_certificacao(self):
        """
        The detail view of a termokk with a pub_date in the past should display
        the termokk do Termokk.
        """
        past_certificacao = create_certificacao(certificado='Past Certificacao.', days=-5)
        response = self.client.get(reverse('CriacaoTermo:detail', args=(past_certificacao.id,)))
        self.assertContains(response, past_certificacao.certificado, status_code=200)
