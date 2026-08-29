SHELL := /bin/bash
INSTALL_DIR = $(HOME)/.vibe/

.PHONY: clean copy-references build install

# Declare only the shared references each skill needs.  Paths are relative to
# the top-level references/ directory and are preserved in the packaged skill.
REFERENCE_SKILLS := writing-specs writing-plans executing-plans writing-github-issues-for-features writing-github-issues-for-bugs reviewing-code reviewing-github-prs
writing-specs_REFERENCES := software-engineering.md
writing-plans_REFERENCES := software-engineering.md
executing-plans_REFERENCES := software-engineering.md code-review-guidelines.md
writing-github-issues-for-features_REFERENCES := github-issue-guidelines.md software-engineering.md
writing-github-issues-for-bugs_REFERENCES := github-issue-guidelines.md software-engineering.md
reviewing-code_REFERENCES := software-engineering.md code-review-guidelines.md learning-equality-guidelines.md
reviewing-github-prs_REFERENCES := software-engineering.md code-review-guidelines.md learning-equality-guidelines.md

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
	git clone git@github.com:ciembor/agent-rules-books.git sources/agent-rules-books
	git clone git@github.com:addyosmani/agent-skills.git sources/agent-skills
	git clone git@github.com:learningequality/le-skills.git sources/le-skills
	git clone git@github.com:obra/superpowers.git sources/superpowers


define MAKE_REFERENCE_RULE
output/skills/$(1)/references/$(2): references/$(2)
	mkdir -p $$(@D)
	cp $$< $$@
endef

$(foreach skill,$(REFERENCE_SKILLS),$(foreach reference,$($(skill)_REFERENCES),$(eval $(call MAKE_REFERENCE_RULE,$(skill),$(reference)))))
