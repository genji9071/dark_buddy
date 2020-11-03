simsimi_url = "https://wsapi.simsimi.com/190410/talk"
simsimi_header = {
    "Content-Type": "application/json",
    "x-api-key": "qDvtLf4pdpSLB8k+wMPN8KIEo6d+NRGQEIW3JrlR"
}


def get_simsimi_body(request):
    return {
        "utext": request,
        "lang": "ch",
        "atext_bad_prob_min": "1.0"
    }
