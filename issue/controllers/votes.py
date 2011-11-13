from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from djangobp.route import render_to_json
from issue.models import Vote, Issue


@login_required
def create(request, resource_id):
    issue = Issue.objects.get(id=request.POST['issue'])

    if (Vote.objects.filter(voter=request.user, issue=issue).count() == 0):
        is_agree = int(request.POST['is_agree'])
        vote = issue.vote_set.create(voter=request.user, is_agree=is_agree)

        return render_to_json({
                    'status':'ok',
                    'vote_score':issue.vote_score,
                    'vote_id':vote.id
        })

    return render_to_json({
        'status':'ignore'
    })

@login_required
def destroy(request, resource_id):
    try:
        vote = Vote.objects.get(id=resource_id)
        issue = vote.issue
        vote.delete()
        return render_to_json({
            'status':'ok',
            'vote_score':issue.vote_score
        })
    except ObjectDoesNotExist:
        return render_to_json({
            'status':'ignore'
        })