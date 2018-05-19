from django.shortcuts import render


def peer(request):
    return render(request, 'peer_review/peer.html', {})
