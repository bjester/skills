SHELL := /bin/bash
INSTALL_DIR = $(HOME)/.vibe/

.PHONY: clean copy-references build install sources

# Declare only the shared references each skill needs.  Paths are relative to
# the top-level references/ directory and are preserved in the packaged skill.
REFERENCE_SKILLS := writing-github-issues-for-features writing-github-issues-for-bugs writing-technical-docs pairing-with-adhd executing-plans
writing-github-issues-for-features_REFERENCES := github-issue-guidelines.md
writing-github-issues-for-bugs_REFERENCES := github-issue-guidelines.md
writing-technical-docs_REFERENCES := word-swaps.md
pairing-with-adhd_REFERENCES := word-swaps.md
executing-plans_REFERENCES := decision-log-template.tsv

REFERENCE_OUTPUTS := $(foreach skill,$(REFERENCE_SKILLS),$(addprefix output/skills/$(skill)/references/,$($(skill)_REFERENCES)))

clean:
	rm -rf output

copy-references: $(REFERENCE_OUTPUTS)

build: clean
	mkdir -p output/skills/
	cp -r skills/* output/skills/
	$(MAKE) copy-references

install: build
	rsync --progress -ah output/ "$(INSTALL_DIR)"

sources:
	mkdir -p sources/
	$(MAKE) sources/agent-rules-books \
		sources/agent-skills \
		sources/cursor-plugins \
		sources/google-skills \
		sources/i-have-adhd \
		sources/le-skills \
		sources/mattpocock-skills \
		sources/security-audit-skill \
		sources/SimpleEnglish \
		sources/superpowers

sources/agent-rules-books:
	git clone git@github.com:ciembor/agent-rules-books.git $@

sources/agent-skills:
	git clone git@github.com:addyosmani/agent-skills.git $@

sources/cursor-plugins:
	git clone git@github.com:cursor/plugins.git $@

sources/google-skills:
	git clone git@github.com:google/skills.git $@

sources/i-have-adhd:
	git clone git@github.com:ayghri/i-have-adhd.git $@

sources/le-skills:
	git clone git@github.com:learningequality/le-skills.git $@

sources/mattpocock-skills:
	git clone git@github.com:mattpocock/skills.git $@

sources/security-audit-skill:
	git clone git@github.com:cloudflare/security-audit-skill.git $@

sources/SimpleEnglish:
	git clone git@github.com:AminBlg/SimpleEnglish.git $@

sources/superpowers:
	git clone git@github.com:obra/superpowers.git $@

define MAKE_REFERENCE_RULE
output/skills/$(1)/references/$(2): references/$(2)
	mkdir -p $$(@D)
	cp $$< $$@
endef

$(foreach skill,$(REFERENCE_SKILLS),$(foreach reference,$($(skill)_REFERENCES),$(eval $(call MAKE_REFERENCE_RULE,$(skill),$(reference)))))
