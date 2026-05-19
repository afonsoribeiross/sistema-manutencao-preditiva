# Sistema de Manutenção Preditiva Industrial

Sistema de monitoramento industrial desenvolvido em Python que antecipa falhas de máquinas antes que aconteçam, monitorando temperatura, vibração e pressão em tempo real e classificando automaticamente o estado operacional da máquina.

🔗 **[Acesse o sistema online](https://sistema-manutencao-preditiva.streamlit.app)**

---

## O Problema

Manutenção reativa — agir só depois que a máquina falha — gera paradas não planejadas, custos elevados e risco operacional. Um sistema de monitoramento contínuo permite identificar anomalias antes que se tornem falhas, reduzindo tempo de parada e custo de manutenção.

## A Solução

Este sistema monitora continuamente os parâmetros críticos de uma máquina industrial e classifica automaticamente seu estado em três níveis:

- 🟢 **Normal** — operação dentro dos limites esperados
- 🟡 **Alerta** — parâmetro se aproximando do limite crítico
- 🔴 **Crítico** — risco de falha iminente, ação necessária

Quando um estado crítico é detectado, o sistema dispara automaticamente um alerta por email via integração com n8n — sem necessidade de intervenção humana para monitoramento.

## Arquitetura

```
Entrada de dados (sensores simulados)
        ↓
Dashboard Streamlit (visualização em tempo real)
        ↓
Classificação automática por thresholds configuráveis
        ↓
Webhook → n8n Cloud
        ↓
Alerta automático por email
```

Os thresholds de classificação são configuráveis e podem ser ajustados conforme requisitos operacionais, histórico da máquina ou normas técnicas aplicáveis ao contexto real de operação.

## Funcionalidades

- Dashboard com gauges estilo painel industrial (temperatura, vibração, pressão)
- Classificação automática de estado em tempo real
- Histórico de leituras com gráfico de evolução temporal
- Detecção de tendências antes do estado crítico
- Alertas automáticos por email via n8n + webhook
- Limites de operação configuráveis por parâmetro

## Stack Técnica

| Camada | Tecnologia |
|---|---|
| Interface | Python + Streamlit |
| Visualização | Matplotlib + NumPy |
| Dados | Pandas |
| Automação | n8n Cloud + Webhooks |
| Deploy | Streamlit Cloud |
| Versionamento | Git + GitHub |

## Diferenciais do Projeto

**Automação real:** o sistema não exige que o operador monitore ativamente o dashboard. A detecção de estado crítico dispara alertas automaticamente via pipeline n8n.

**Thresholds configuráveis:** os limites de alerta não são fixos. O sistema foi projetado para ser adaptável a diferentes máquinas, contextos operacionais e normas técnicas.

**Visão de engenharia:** o projeto foi desenvolvido com foco em aplicabilidade industrial real — não apenas como exercício acadêmico, mas como protótipo funcional de um sistema que indústrias como Alcoa, Ambev e Vale utilizam em escala.

## Próximas Etapas

- [ ] Integração com sensores físicos via MQTT ou API
- [ ] Relatório automático em PDF gerado pelo sistema
- [ ] Painel de configuração de thresholds pela interface
- [ ] Histórico persistente em banco de dados

## Sobre o Projeto

Desenvolvido por **Afonso Ribeiro** — aplicando programação e automação a problemas reais de engenharia.

[![GitHub](https://img.shields.io/badge/GitHub-afonsoribeiross-181717?logo=github)](https://github.com/afonsoribeiross)
