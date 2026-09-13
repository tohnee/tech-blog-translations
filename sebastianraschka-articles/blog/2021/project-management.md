---
title: "How I Keep My Projects Organized"
source: https://sebastianraschka.com/blog/2021/project-management.html
crawled: 2026-09-06
---

# How I Keep My Projects Organized

---

## Motivation

Since I started my undergraduate studies in 2008, I have been obsessed with productivity tips, notetaking solutions, and todo list management. Over the years, I tried many, many workflows and hundreds of (mostly digital) tools to keep my life, projects, and notes organized.

Occasionally, I exchange ideas with friends and colleagues, and upon request, I talked about my workflow a couple of times on Twitter. After today’s 2021-edition of this discussion, I thought that writing a quick and informal blogpost makes sense, making it easier to read and having a quick reference if someone asks about it again :).

[![Drawing](https://sebastianraschka.com/images/blog/2021/project-management/twitter.webp)](https://twitter.com/rasbt/status/1345874138754375680)

Overall, my approach is inspired by David Allen’s [Getting Things Done](https://gettingthingsdone.com). Also, it is a mostly digital workflow with some pen & paper elements. After many years of experimentation with dedicated tools and other workflows, I have been using it without major change or modification for approximately four years now, and it works well for me.

Personally, my philosophy is to avoid subscriptions and dedicated tools that lock you into particular services or ecosystems (which may or may not exist in a few years). Also, as I am using two computers, my data needs to be synced across devices. Another requirement is that everything should be easy to backup.

Please note that this informal write-up is primarily to provide a more detailed version of my approach to “those who asked,” and if you already have a good system, I recommend you to stick with it. Sticking with one system is probably the most important productivity advice because much time can be wasted on the quest for the (non-existing) perfect tool or workflow.

## Project Folders

In essence, my project management is centered around a so-called “`project-data`” folder, where I keep all my active projects. These are the projects that I am currently working on. Each project has a separate folder inside the `project-data` folder, which is prefixed with a category, for instance,

- `admin__`: various administrative things (like my website, but also recommendation letters, etc.);
- `paper__`: papers I am currently working on;
- `grant__`: grant applications I am working towards;
- `learn__`: things I am currently studying (books or online courses);
- `maybe__`: for projects that may be fun but are currently a distraction, or something I may want to keep in the back of my head and want to get back to later;
- …
- `talk__`: talks I am going to give;
- `trips__`: travel-related material for upcoming trips;
- `write__`: writing projects that are not research papers (books, book chapters, or blog posts).

![Drawing](https://sebastianraschka.com/images/blog/2021/project-management/project-data-1.webp)

In each folder, I keep project-relevant files, which differ across projects. Examples include papers to read, meeting notes, receipts, figures, and weblinks. For instance, if the project includes writing collaboratively on Overleaf, I would include a weblink to the Overleaf project in the main folder. Also, each of these folders contains a project todo list managing the todos for each project. I add information about due dates in these files and add them to my calendar (including reminders).

![Drawing](https://sebastianraschka.com/images/blog/2021/project-management/project-contents.webp)

Sometimes, I use plain text files for the todo lists. Sometimes I use Markdown files Pages documents if I include LaTeX equations or want to drag-and-drop images or screenshots. Now, I also often use a OneNote page because of the nice checkboxes that can easily be reordered and then include a link to the OneNote page in my folder (one downside is that backups can become a problem – more on Backups later). Overall, I use the tool that is best suited for making the project’s todo list.

![Drawing](https://sebastianraschka.com/images/blog/2021/project-management/one-note.webp)

I will explain more about how I use these todo lists later in the sections “Weekly Review” and “Daily Todo Lists and Time Blocking” later.

## Project Archival

In addition to the aforementioned `project-data` folder, I keep a `project-archive` folder (going back to my Bachelor thesis in 2011) containing my completed projects.

![Drawing](https://sebastianraschka.com/images/blog/2021/project-management/project-archive-old.webp)

Upon completion of a project, I would go through the project folder inside the `project-data` folder and make sure I have all the relevant files on my computer. For example, if the project-todo list is on OneNote, I would export it as PDF, or I would download the LaTeX source files if I used Overleaf for a collaborative writing project. Then, I prefix the project with the year and month it was completed and move it to my `project-archive` folder.

![Drawing](https://sebastianraschka.com/images/blog/2021/project-management/project-archive.webp)

## Weekly Review

Every week I review my active projects. Typically, I spend approximately 30-60 min on this every Sunday night; sometimes, I defer it and do it first thing Monday morning. During the review, I go through my project folders in`project-data`, focusing on the projects’ todo lists. I check off items that I finished in the previous week, and occasionally I reorganize projects. From these todo lists, I compile a weekly todo list of things I want to/need to get done and want to accomplish.

![Drawing](https://sebastianraschka.com/images/blog/2021/project-management/weekly-todo.webp)

While I also refer to the project todo-files during the week, this weekly todo list is my main todo list for a given week. I usually use this to make my daily todo lists, for which I use time blocking, which I explain in the next section.

Usually, I print my weekly todo list so that I can scribble on it (crossing out things with a pen is oddly satisfying) and can add new todo lists at the bottom of the list. Unless it is something urgent, I try to do these new todo list items last.

## Daily Todo Lists and Time Blocking

Each evening, I look at my calendar and weekly todo list to design my work plan for the coming day. When I remember correctly, I think my time blocking approach was inspired by Cal Newport’s [Deep Habits: The Importance of Planning Every Minute of Your Work Day](https://www.calnewport.com/blog/2013/12/21/deep-habits-the-importance-of-planning-every-minute-of-your-work-day/).

I use a loose piece of paper (which I collect and scan later for archival purposes) and draw out my meetings and things I want to work on that day. Often, I do not strictly stick to it and sometimes even cancel items because other things took longer or urgent things came up. However, what’s nice about having a plan is that it gives me a rough idea of what is doable in a given day, and it helps me keep expectations manageable.

![Drawing](https://sebastianraschka.com/images/blog/2021/project-management/daily.webp)

## Syncing Project Data Across Machines

I like to have all my projects accessible on all my (two) computers. (This was more important pre-COVID when I alternated between my campus and home office and traveled.) For this, I am using Microsoft OneDrive, but other cloud-syncing services probably work equally well.

![Drawing](https://sebastianraschka.com/images/blog/2021/project-management/onedrive.webp)

On my main computer, I have all the project data available offline. For my smaller-storage laptop, I can download data via the “Files On-Demand” option. I do not work on/from mobile devices like my iPhone and iPad – I only use the former for navigation, two-factor auth, essential phone functions, and the latter for teaching. However, I assume that this cloud-sync approach would also allow one to more from mobile devices (e.g., via a OneDrive app).

## Backups

I find that keeping active and archived projects in folder structures makes the implementation of regular backups relatively straightforward. I use (maybe too) many backup solutions to have some redundancy. Besides having the project data in the cloud, I use the TimeMachine on macOS to back up my computer to physical disks and [Arq](https://www.arqbackup.com) to create additional time-stamped backups with another cloud provider. Also, starting last year, I copy my active and archived projects to an SD card that I keep in a secure location.

![Drawing](https://sebastianraschka.com/images/blog/2021/project-management/sd-card.webp)

My tip for having good backups is to walk through the hypothetical scenarios:

- my apartment/house is flooded or burns down;
- my computer is stolen or destroyed;
- my office is flooded or burns down.
- what happens if cloud-provider X is unreliable and uses my data

If you have a plan for recovering your data in each of the scenarios listed above, you are probably OK.

## Long Term Notes

For keeping notes (e.g., generally interesting tidbits from papers) long term, I use a personal wiki based on [DokuWiki](https://www.dokuwiki.org/dokuwiki). If you already have a webserver for your personal website, this approach is a free and proven solution – I don’t think a DokuWiki will become obsolete any time soon.

![Drawing](https://sebastianraschka.com/images/blog/2021/project-management/wiki.webp)

## Conclusion

Please note that the workflow I outlined above is something that works particularly well for me, but your mileage may differ. What I particular like is that it allows and enables

- offline work (sometimes, I like to turn off the internet to improve focus);
- easy & selective sync across devices (because I have multiple computers);
- easy backups (for peace of mind).

Also,

- there is no strong ecosystem lock-in (switching tools or even OS’s in the future is not a problem);
- it is largely free :);
- and it allows me to use specific tool(s) for each project while still keeping organization and archival straightforward.

Overall, I think one of the keys to good productivity is to find an approach that works relatively well for you and sticking with it, to avoid anxiety through constantly switching things and searching for something better. It may not hurt to reevaluate your approach every 5-10 years or so :).
