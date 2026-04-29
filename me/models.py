from django.db import models


class Link(models.Model):
    name = models.CharField(max_length=100)
    link = models.URLField()
    icon_class = models.CharField(max_length=100)
    order = models.IntegerField(default=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "링크"
        verbose_name_plural = "링크"


class Expression(models.Model):
    keyword = models.CharField(max_length=100)
    order = models.IntegerField(default=100)

    def __str__(self):
        return self.keyword

    class Meta:
        verbose_name = "내소개 표현"
        verbose_name_plural = "내소개 표현"


class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=100)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "보유기술"
        verbose_name_plural = "보유기술"


class Career(models.Model):
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    introduction = models.CharField(max_length=255, blank=True)
    summary = models.CharField(max_length=255, blank=True)
    skills = models.ManyToManyField(Skill)

    def __str__(self):
        return self.company

    class Meta:
        verbose_name = "경력"
        verbose_name_plural = "경력"


class CareerProject(models.Model):
    career = models.ForeignKey(Career, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    introduction = models.CharField(max_length=255, blank=True)

    period = models.CharField(max_length=30, blank=True)
    content = models.TextField(blank=True)
    result = models.TextField(blank=True)
    order = models.IntegerField(default=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "경력 프로젝트"
        verbose_name_plural = "경력 프로젝트"


class CareerProjectFile(models.Model):
    career_project = models.ForeignKey(CareerProject, on_delete=models.CASCADE)
    file = models.FileField(upload_to='career_projects/%Y/%m/%d', blank=True)

    class Meta:
        verbose_name = "경력 프로젝트 참고자료"
        verbose_name_plural = "경력 프로젝트 참고자료"


class Others(models.Model):
    """
    기타 사항 모델입니다. 예를 들어, 학력, 자격증, 수상 경력, 외국어 능력 등을 저장할 수 있습니다.
    """
    period = models.CharField(max_length=30, blank=True)
    name = models.CharField(max_length=100, help_text="학교/전공, 자격증명 등 두꺼운 폰트")
    content = models.CharField(max_length=100, help_text="졸업 상태, 발급 기관 등 회색 폰트")

    order = models.IntegerField(default=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "기타 사항"
        verbose_name_plural = "기타 사항"


class Project(models.Model):
    title = models.CharField(max_length=100)
    introduction = models.CharField(max_length=255, blank=True)
    order = models.IntegerField(default=100)

    content = models.TextField(blank=True)
    result = models.TextField(blank=True)
    skills = models.ManyToManyField(Skill)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "프로젝트"
        verbose_name_plural = "프로젝트"


class ProjectUrl(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = "프로젝트 URL"
        verbose_name_plural = "프로젝트 URL"


class ProjectFile(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    file = models.FileField(upload_to='projects/%Y/%m/%d', blank=True)

    class Meta:
        verbose_name = "프로젝트 이미지"
        verbose_name_plural = "프로젝트 이미지"


class Resume(models.Model):
    title = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100)
    birth = models.DateField()

    profile_image = models.ImageField(upload_to="profile_images/")
    introduction = models.TextField()
    email = models.EmailField()
    is_represented = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    links = models.ManyToManyField(Link, through="ResumeLink")
    expressions = models.ManyToManyField(Expression, through="ResumeExpression")
    skills = models.ManyToManyField(Skill, through="ResumeSkill")
    careers = models.ManyToManyField(Career, through="ResumeCareer")
    projects = models.ManyToManyField(Project, through="ResumeProject")
    others = models.ManyToManyField(Others, through="ResumeOthers")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-is_represented", "name"]
        verbose_name = "이력서"
        verbose_name_plural = "이력서"


class ResumeOthers(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    others = models.ForeignKey(Others, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=100)


class ResumeLink(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=100)


class ResumeProject(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    order = models.IntegerField(default=100)


class ResumeSkill(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    order = models.IntegerField(default=100)


class ResumeCareer(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    career = models.ForeignKey(Career, on_delete=models.CASCADE)


class ResumeExpression(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    expression = models.ForeignKey(Expression, on_delete=models.CASCADE)
    order = models.IntegerField(default=100)
