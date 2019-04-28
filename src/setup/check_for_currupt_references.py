from engine.api import API
from engine.utils.printing_utils import progressBar
from setup.utils.datastore_utils import repair_corrupt_reference, link_references_to_paper


def remove_duplicates_from_cited_by():
    print("\nRemove Duplicates")
    api = API()
    papers = api.get_all_paper()

    for i, paper in enumerate(papers):
        progressBar(i, len(papers))
        paper.cited_by = list(dict.fromkeys(paper.cited_by))
        api.client.update_paper(paper)


def check_references():
    print("\nCheck References")
    api = API()
    papers = api.get_all_paper()

    for i, paper in enumerate(papers):
        progressBar(i, len(papers))

        other_papers = [p for p in papers if p.id != paper.id]
        for reference in paper.references:
            if not reference.get_paper_id():
                continue

            ref_paper = api.get_paper(reference.get_paper_id())
            if ref_paper.cited_by.count(paper.id) == 0:
                print()
                reference.paper_id = []
                api.client.update_paper(paper)
                repair_corrupt_reference(reference, paper, other_papers, api)


def check_cited_by():
    print("\nCheck Cited by")
    api = API()
    papers = api.get_all_paper()

    for i, paper in enumerate(papers):
        progressBar(i, len(papers))
        for cited_paper_id in paper.cited_by:
            if not api.contains_paper(cited_paper_id):
                paper.cited_by.remove(cited_paper_id)
                api.client.update_paper(paper)
                continue

            cited_paper = api.get_paper(cited_paper_id)
            cited_paper_refs = [ref.get_paper_id() for ref in cited_paper.references if ref.get_paper_id()]

            if cited_paper_refs.count(paper.id) == 0:
                print()
                paper.cited_by.remove(cited_paper_id)
                api.client.update_paper(paper)
                link_references_to_paper(cited_paper, paper, api)


def perform_checks():
    check_cited_by()
    remove_duplicates_from_cited_by()
    check_references()


if __name__ == "__main__":
    perform_checks()
    exit(0)
