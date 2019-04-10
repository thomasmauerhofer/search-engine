from difflib import SequenceMatcher


def __check_similarity(ref, paper, other_paper, api):
    similarity = SequenceMatcher(None, ref.complete_ref_raw.lower(), other_paper.title_raw.lower()).ratio()
    if similarity >= 0.49:
        choice = ''
        while choice.lower() != 'y' and choice.lower() != 'n' and choice.lower() != "exit":
            choice = input(
                "{}\n ---> {}\n(y/n)".format(other_paper.title_raw.lower(), ref.complete_ref_raw.lower()))

        if choice.lower() == 'y':
            ref.paper_id = [other_paper.id, "manual"]
            api.client.update_paper(paper)
            other_paper.cited_by.append(paper.id)
            api.client.update_paper(other_paper)
            return True
        elif choice.lower() == 'n':
            return False
        elif choice.lower() == 'exit':
            print("bye!")
            exit(0)


def link_references_to_paper(paper, other_paper, api):
    if not other_paper.title_raw:
        return

    for ref in paper.references:
        if ref.paper_id:
            continue

        if __check_similarity(ref, paper, other_paper, api):
            continue


def repair_corrupt_reference(ref, paper, other_papers, api):
    for other_paper in other_papers:
        if __check_similarity(ref, paper, other_paper, api):
            return
