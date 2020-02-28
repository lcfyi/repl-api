COPY code /

RUN echo -e "\n/exit\n" >> code

RUN touch b.sh
RUN echo "#!/bin/sh" > b.sh
RUN echo "cat code" >> b.sh
RUN echo "jshell code" >> b.sh
RUN chmod +x b.sh

CMD ["sh", "b.sh"]
